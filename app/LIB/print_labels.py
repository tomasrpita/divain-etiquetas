import os
from dataclasses import dataclass
import logging
from typing import Callable, List
import win32print
from app.LIB.printers import get_printer_list
from app.LIB.utils import get_printers

log = logging.getLogger(__name__)


def get_printers():
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_CONNECTIONS + win32print.PRINTER_ENUM_LOCAL
    )
    port_to_printer = {}
    for printer in printers:
        printer_name = printer[2]
        try:
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
                printer_info = win32print.GetPrinter(hPrinter, 2)
                port_name = printer_info["pPortName"]
                port_to_printer[port_name] = printer_name
            finally:
                win32print.ClosePrinter(hPrinter)
        except Exception as e:
            log.error(f"Failed to get printer info for {printer_name}: {e}")
    return port_to_printer


port_to_printer = get_printers()

log.debug(f"port_to_printer: {port_to_printer}")

PUERTOS_IMPRESORAS = {
    "USB001": port_to_printer.get("USB001", "default_printer"),
    "USB002": port_to_printer.get("USB002", "codebar_printer"),
    "USB003": port_to_printer.get("USB003", "black_printer"),
}


def get_printer_by_port(port: str):
    print(f"Printer for port {port}: {printer}")
    log.debug(f"Printer for port {port}: {printer}")
    return PUERTOS_IMPRESORAS.get(port, "default_printer")


def printer_job(printer_name, printer_file):
    log.debug(f"Attempting to print on printer: {printer_name}")
    print(f"Attempting to print on printer: {printer_name}")
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Print job", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, printer_file)
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)


# UE - UK - USA- MX
destinations = {
    "UE": {
        "destination": "UE",
        "ingredient_lines": {
            "start": 37,
            "end": 46,
        },
        "lote_bottle_line": 22,
        "lote_box_line": 48,
        "sku_box_line": 47,
        "barcode_box_line": 49,
        "ean_box_line": 50,
        "copies_number_line": 51,
        "file": "ue-bottle-box-codebar.prn",
        "QR_box_line": 36,
    },
    "UK": {
        "destination": "UK",
        "ingredient_lines": {
            "start": 26,
            "end": 35,
        },
        "lote_bottle_line": 16,
        "lote_box_line": 37,
        "sku_box_line": 36,
        "barcode_box_line": 38,
        "ean_box_line": 39,
        "copies_number_line": 40,
        "file": "uk-bottle-box-codebar.prn",
        "QR_box_line": 25,
    },
    "USA": {
        "destination": "USA",
        "ingredient_lines": {
            "start": 36,
            "end": 45,
        },
        "lote_bottle_line": 21,  # for no print
        "lote_box_line": 47,
        "sku_box_line": 46,
        "barcode_box_line": 48,
        "ean_box_line": 49,
        "copies_number_line": 50,
        "file": "usa-bottle-box-codebar.prn",
        "QR_box_line": 35,
    },
    "MX": {
        "destination": "MX",
        "file": "mx-bottle-box-codebar.prn",
    },
}


def split_text(text: str, max_line_chr: int) -> List[str]:
    """
    Split text in lines with max_line_chr characters
    """
    words = text.split(" ")
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) > max_line_chr:
            lines.append(line)
            line = word
        else:
            line += " " + word
    lines.append(line.strip())
    return lines


def index_exists(list: List, index: int) -> bool:
    """
    Check if index exists in list
    """
    return index < len(list) and index >= 0


class PrinterLabels:
    def __init__(self, formdata, printer_job, pro=False) -> None:
        self.copies_mumber = (
            int(formdata["CopiesNumber"]) if formdata["CopiesNumber"] else 0
        )
        self.lote = formdata["loteBotella"]
        self.ean_botes = formdata["ean_botes"]
        self.ean_muestras = formdata["ean_muestras"]
        self.numero_divain = formdata["numero_divain"]
        self.copies_mumber = formdata["CopiesNumber"]
        self.sex = formdata["sexo"]
        self.sku = formdata["sku"]
        self.categoria = formdata["categoria"]
        self.ingredientes = formdata["ingredientes"]
        self.free_sample = formdata.get("free_sample")
        self.tsc_label = (
            formdata["tscLabel"] if formdata["tscLabel"] != "ninguna" else ""
        )
        self.zd_label = formdata.get("zdLabel")
        self.fragance_name = formdata.get("fragance_name")
        self.label_destination = formdata.get("label_destination")
        self.printer_job = printer_job
        self.pro = pro
        self.fecha = self.extract_date_from_ean(formdata["eanBotella"])
        print(formdata)

    def extract_date_from_ean(self, ean):
        # Buscar el código de fecha que sigue a ')17='
        try:
            date_code = ean.split(")17=")[1][
                :6
            ]  # Los primeros 6 caracteres después de ')17='
            return date_code
        except IndexError:
            # Manejar el caso donde no se encuentra la fecha o el formato es incorrecto
            print("Formato de fecha incorrecto o inexistente en eanBotella.")
            return None

    def print_bottle_label_standard_new(self):
        if (
            self.sex == "H O M M E" or self.categoria == "black"
        ) and self.categoria != "ken":
            printer = get_printer_by_port("USB003")
        elif self.sex == "U N I S E X" and (
            ("001" <= self.numero_divain <= "049")
            or ("200" <= self.numero_divain <= "499")
        ):
            printer = get_printer_by_port("USB003")
        else:
            printer = get_printer_by_port("USB001")

        if not printer:
            log.error("No printer found for the specified port.")
            return

        pl = get_printer_list()
        for p in pl:
            print(f"Printer: {p}")

        print(f"Printing bottle label on printer: {printer}")

        if self.fragance_name == "HOPE":
            label_file = "./labels/nueva-home-hope.prn"
        elif self.fragance_name == "REBEL":
            label_file = "./labels/nueva-home-rebel.prn"
        elif self.fragance_name == "FEELING":
            label_file = "./labels/nueva-home-feeling.prn"
        elif self.fragance_name == "PLEASURE":
            label_file = "./labels/nueva-home-pleasure.prn"
        elif self.fragance_name == "PALO SANTO":
            label_file = "./labels/nueva-home-palo-santo.prn"
        elif self.fragance_name == "DARK AMBER":
            label_file = "./labels/nueva-home-dark-amber.prn"
        elif self.fragance_name == "TRUE LEATHER":
            label_file = "./labels/nueva-home-true-leather.prn"
        elif self.fragance_name == "GEORGEOUS SANDALWOOD":
            label_file = "./labels/nueva-home-georgeous-sandalwood.prn"
        elif self.fragance_name == "PETAL POP":
            label_file = "./labels/nueva-home-petal-pop.prn"
        elif self.fragance_name == "MYSTIC":
            label_file = "./labels/nueva-home-mystic.prn"
        elif self.fragance_name == "SAKURA DREAM":
            label_file = "./labels/nueva-home-sakura-dream.prn"
        elif self.fragance_name == "ZEN":
            label_file = "./labels/nueva-home-zen.prn"
        elif self.fragance_name == "VANILLA BEAN":
            label_file = "./labels/nueva-home-vanilla-bean.prn"
        elif self.fragance_name == "VELVET CREAM":
            label_file = "./labels/nueva-home-velvet-cream.prn"
        elif self.fragance_name == "AMBER LUXE":
            label_file = "./labels/nueva-home-amber-luxe.prn"
        elif self.fragance_name == "OREGANIC":
            label_file = "./labels/nueva-home-oreganic.prn"
        elif self.fragance_name == "BEETROOT BLAST":
            label_file = "./labels/nueva-home-beetroot-blast.prn"
        elif self.fragance_name == "TOMATO KICK":
            label_file = "./labels/nueva-home-tomato-kick.prn"
        elif self.fragance_name == "HERBAL ELIXIR":
            label_file = "./labels/nueva-home-herbal-elixir.prn"
        elif self.fragance_name == "CARIBIC PIRATES":
            label_file = "./labels/nueva-home-caribic-pirates.prn"
        elif self.fragance_name == "BOLD SPIRIT":
            label_file = "./labels/nueva-home-bold-spirit.prn"
        elif self.categoria == "oriental":
            label_file = "./labels/nueva-zzzz-oriental.prn"
        elif self.categoria == "ken":
            label_file = "./labels/nueva-ken.prn"
        elif self.categoria == "barbie":
            label_file = "./labels/nueva-barbie.prn"
        elif self.categoria == "black":
            label_file = "./labels/nueva-black.prn"
        elif self.sex == "K I D S":
            label_file = "./labels/nueva-kids.prn"
        else:
            label_file = "./labels/nueva.prn"

        with open(label_file, "rb") as f:
            s = f.read()

        if self.categoria == "black":
            sex_text = "black edition"
        elif self.sex == "F E M M E":
            sex_text = "for her"
        elif self.sex == "H O M M E":
            sex_text = "for him"
        elif self.sex == "U N I S E X":
            sex_text = "for all"
        else:
            sex_text = ""

        s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))
        s = s.replace(b"for XXX", bytes(sex_text, "utf-8"))
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber},1", "utf-8"))

        try:
            print_content = s.decode("utf-8")
            print("Contenido enviado a la impresora:")
        except UnicodeDecodeError:
            print("Contenido en bytes; no se puede mostrar como texto.")

        self.printer_job(printer, s)

    def print_destination_group_label(self, labels_info: dict):
        printer = get_printer_by_port("USB002")
        if not printer:
            log.error("No printer found for the specified port.")
            return

        base_dir = "./labels/"
        self.copies_mumber = 45 if self.pro else self.copies_mumber

        if labels_info["destination"] == "MX":
            f = open(os.path.join(base_dir, labels_info["file"]), "rb")
            s = f.read()
            f.close()

            s = s.replace(b"XXXXXX", bytes(f"{self.lote}", "utf-8"))
            s = s.replace(b"DIVAIN-ZZZ", bytes(f"{self.sku}", "utf-8"))
            s = s.replace(b"xxxxxxxxxx", bytes(f"{self.lote}", "utf-8"))
            ean_select = self.ean_botes[:-1] + "!100" + self.ean_botes[-1:]
            s = s.replace(b"123456789012!1003", bytes(ean_select, "utf-8"))
            s = s.replace(b"1234567890123", bytes(f"{self.ean_botes}", "utf-8"))
            s = s.replace(
                b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8")
            )

            qr_data = f"(01){self.ean_botes}(10){self.lote}(17){self.fecha}"
            qr_bytes = bytes(qr_data, "utf-8")
            s = s.replace(b"YYYY", qr_bytes)

        else:
            f = open(os.path.join(base_dir, labels_info["file"]), "rb")
            s = f.read()
            f.close()

            line_length = 30
            lista_ingredientes = split_text(self.ingredientes, line_length)

            with open(os.path.join(base_dir, labels_info["file"]), "rb") as f:
                for line_number, line in enumerate(f, start=1):
                    if (
                        labels_info["ingredient_lines"]["start"]
                        <= line_number
                        <= labels_info["ingredient_lines"]["end"]
                    ):
                        index = line_number - labels_info["ingredient_lines"]["start"]
                        print(index)
                        if index_exists(lista_ingredientes, index):
                            s = s.replace(
                                line,
                                (
                                    line.replace(
                                        b"####################",
                                        bytes(lista_ingredientes[index], "utf-8"),
                                    )
                                ),
                            )
                        else:
                            s = s.replace(line, b"")

                    elif line_number == labels_info["lote_bottle_line"]:
                        s = s.replace(
                            line, (line.replace(b"XXXXXX", bytes(self.lote, "utf-8")))
                        )

                    elif line_number == labels_info["sku_box_line"]:
                        s = s.replace(
                            line,
                            (line.replace(b"DIVAIN-ZZZ", bytes(self.sku, "utf-8"))),
                        )

                    elif line_number == labels_info["barcode_box_line"]:
                        ean_select = self.ean_botes[:-1] + "!100" + self.ean_botes[-1:]
                        s = s.replace(
                            line,
                            (
                                line.replace(
                                    b"123456789012!1003", bytes(ean_select, "utf-8")
                                )
                            ),
                        )

                    elif line_number == labels_info["ean_box_line"]:
                        s = s.replace(
                            line,
                            (
                                line.replace(
                                    b"1234567890123", bytes(self.ean_botes, "utf-8")
                                )
                            ),
                        )

                    elif line_number == labels_info["lote_box_line"]:
                        s = s.replace(
                            line,
                            (line.replace(b"xxxxxxxxxx", bytes(self.lote, "utf-8"))),
                        )

                    elif line_number == labels_info["copies_number_line"]:
                        s = s.replace(
                            line,
                            (
                                line.replace(
                                    b"1,1", bytes(f"{self.copies_mumber},1", "utf-8")
                                )
                            ),
                        )

                    elif line_number == labels_info["QR_box_line"]:
                        qr_data = f"(01){self.ean_botes}(10){self.lote}(17){self.fecha}"
                        qr_bytes = bytes(qr_data, "utf-8")
                        s = s.replace(line, line.replace(b"YYYY", qr_bytes))

        self.printer_job(printer, s)

    def print(self):
        tipo_ean = self.ean_botes or self.ean_muestras

        avoid_print_bottle_skus = []
        if self.sku.endswith(tuple(avoid_print_bottle_skus)):
            pass

        elif self.tsc_label == "bottle":
            if (
                self.categoria == "divain"
                or "home"
                and self.sex
                in [
                    "F E M M E",
                    "H O M M E",
                    "U N I S E X",
                    "K I D S",
                    "H O M E",
                ]
            ):
                self.print_bottle_label_standard_new()

        else:
            print("Ninguna: ", get_printer_by_port("USB001"))

        if self.zd_label == "destination_group":
            if self.label_destination in destinations.keys():
                self.print_destination_group_label(destinations[self.label_destination])
            else:
                log.error("Destino no válido")
        else:
            print("Ninguna: ", get_printer_by_port("USB002"))


class PrintManager:
    def __init__(self, print_data: dict, printer: Callable) -> None:
        self.copies_mumber = print_data.get("CopiesNumber", 1)
        self.printer = printer
        self.labels_jobs = [
            ("USB001", self.get_principal_label(print_data)),
            ("USB002", self.get_barcode_label(print_data)),
        ]

    def get_principal_label(self, print_data: dict) -> bytes or None:
        log.debug("get_principal_label - xImplementar")
        return None

    def get_barcode_label(self, print_data: dict) -> bytes or None:
        if print_data.get("zd_label", "") == "ninguna":
            return None

        printer_file = "./printer_labels/new_codigo_barras.prn"
        tipo_ean = print_data.get("ean_botes") or print_data.get("ean_muestras")
        sku = print_data.get("sku")

        try:
            if not tipo_ean:
                raise ValueError("No hay tipo de ean")

            ean_select = tipo_ean[:-1] + ">6" + tipo_ean[-1:]

            with open(printer_file, "rb") as f:
                label = f.read()

            label = label.replace(b"DIVAIN-XXX", bytes(sku, "utf-8"))
            label = label.replace(b"123456789012>63", bytes(ean_select, "utf-8"))
            label = label.replace(b"1234567890123", bytes(tipo_ean, "utf-8"))
            label = label.replace(
                b"^PQ1,0,1,Y", bytes(f"^PQ{self.copies_mumber },0,1,Y", "utf-8")
            )

            return label

        except Exception as e:
            log.error(f"Error al intentar generar etiqueta de código de barra {e}")
            return None

    def print(self) -> None:
        for port, label in self.labels_jobs:
            if label:
                printer = get_printer_by_port(port)
                if printer:
                    self.printer(printer, label)
                else:
                    log.error(f"No printer found for port {port}")


@dataclass
class ReferenceLabelData:
    sku: str
    ean_botes: str
    ean_muestras: str


@dataclass
class PrintJobData:
    copies_number: int
    label_type: str or None
    print_barcode: bool
