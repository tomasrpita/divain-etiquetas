# coding: utf-8

# from app.LIB.printers import printer_job
from dataclasses import dataclass
import logging
from typing import Callable, List
from app.LIB.utils import get_printers


log = logging.getLogger(__name__)
default_printer, codebar_printer = get_printers()


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


# TODO Si hay mas de 15 lineas de ingredientes avisar que no se puede imprimir
class PrinterLabels:
    def __init__(self, formdata, printer_job) -> None:

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
        # self.free_sample = True if  formdata.get('free_sample') else False
        self.free_sample = formdata.get("free_sample")
        self.tsc_label = (
            formdata["tscLabel"] if formdata["tscLabel"] != "ninguna" else ""
        )
        self.zd_label = formdata["zdLabel"] if formdata["zdLabel"] != "ninguna" else ""
        self.printer_job = printer_job

    def print_sample_label_test(self):
        printer = default_printer

        f=open("./printer_labels/new_sample_label_test.prn", "rb")

        # f=open("./printer_labels/new_sample_label.prn", "rb")
        s=f.read()
        f.close()

        self.ean_13 = self.ean_muestras or self.ean_botes

        # number
        s=s.replace(b'XXX', bytes(self.sku.replace('DIVAIN-', ''), 'utf-8'))

        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))

        #barcode
        ean_13 = self.ean_13[:-1] + '!100' + self.ean_13[-1:]
        s=s.replace(b'123456789012!1003', bytes(ean_13, 'utf-8'))

        #copies number
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))

        self.printer_job(printer, s)

        # if self.free_sample == "free":
        #     if self.sex == "H O M M E":
        #         f = open("./printer_labels/new_free_sample_homme.prn", "rb")
        #     else:
        #         f = open("./printer_labels/new_free_sample.prn", "rb")

        # elif self.free_sample == "standard":
        #     if self.sex == "H O M M E":
        #         f = open(
        #             f"./printer_labels/new_sample_{self.categoria}_homme.prn", "rb"
        #         )
        #     else:
        #         f = open(f"./printer_labels/new_sample_{self.categoria}.prn", "rb")

        # elif self.free_sample == "pack":
        #     if self.sex == "H O M M E":
        #         f = open(f"./printer_labels/new_sample_{self.categoria}_pack.prn", "rb")
        #     else:
        #         f = open(f"./printer_labels/new_sample_{self.categoria}_pack.prn", "rb")

        # s = f.read()
        # f.close()

        # # number
        # s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # # sex
        # s = s.replace(b"X X X X X", bytes(self.sex, "utf-8"))

        # # barcode
        # ean_muestras = self.ean_muestras[:-1] + "!100" + self.ean_muestras[-1:]
        # s = s.replace(b"123456789012!1003", bytes(ean_muestras, "utf-8"))

        # # copies number
        # s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        # self.printer_job(printer, s)

    def print_sample_label(self):
        printer = default_printer

        # f=open("./printer_labels/new_sample_label.prn", "rb")

        if self.free_sample == "free":
            if self.sex == "H O M M E":
                f = open("./printer_labels/new_free_sample_homme.prn", "rb")
            else:
                f = open("./printer_labels/new_free_sample.prn", "rb")

        elif self.free_sample == "standard":
            if self.sex == "H O M M E":
                f = open(
                    f"./printer_labels/new_sample_{self.categoria}_homme.prn", "rb"
                )
            else:
                f = open(f"./printer_labels/new_sample_{self.categoria}.prn", "rb")

        elif self.free_sample == "pack":
            if self.sex == "H O M M E":
                f = open(f"./printer_labels/new_sample_{self.categoria}_pack.prn", "rb")
            else:
                f = open(f"./printer_labels/new_sample_{self.categoria}_pack.prn", "rb")

        s = f.read()
        f.close()

        # number
        s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # sex
        s = s.replace(b"X X X X X", bytes(self.sex, "utf-8"))

        # barcode
        ean_muestras = self.ean_muestras[:-1] + "!100" + self.ean_muestras[-1:]
        s = s.replace(b"123456789012!1003", bytes(ean_muestras, "utf-8"))

        # copies number
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        self.printer_job(printer, s)

    def print_box_label(self, tipo_ean):
        printer = codebar_printer
        # printer = 'ZDesigner ZD420-203dpi ZPL'

        f = open("./labels/codigo_barras_ingredientes_usa.prn", "r")
        s = f.read()
        f.close()

        line_length = 20
        lista_ingredientes = split_text(self.ingredientes, line_length)
        # print('Número de lineas de ingredientes: ', len(lista_ingredientes))
        # print('Número de ingredientes: ', len(self.ingredientes.split(' ')))

        # read line by line ''s'' and replace the text
        with open("./labels/codigo_barras_ingredientes_usa.prn", "r") as f:
            # s = f.read()
            for line_number, line in enumerate(f, start=1):
                # SKU
                # lista de ingredientes
                if 13 <= line_number <= 20:
                    if index_exists(lista_ingredientes, line_number - 12):
                        s = s.replace(
                            line,
                            (
                                line.replace(
                                    "XXXXXXXXXXXXXXXXX", lista_ingredientes[line_number - 12]
                                )
                            ),
                        )
                    else:
                        s = s.replace(line, "")
                elif line_number == 21 or line_number == 22:
                    s = s.replace(line, (line.replace("DIVAIN-ZZZ", self.sku)))
                # LOTE
                elif line_number == 23 or line_number == 24:
                    s = s.replace(line, (line.replace("xxxxxxxxxx", self.lote)))
                # BAR CODE
                elif line_number == 25:
                    ean_select = tipo_ean[:-1] + "!100" + tipo_ean[-1:]
                    s = s.replace(line, (line.replace("123456789012!1003", ean_select)))
                # Núnmero código de barras
                elif line_number == 26:
                    s = s.replace(line, (line.replace("1234567890123", tipo_ean)))

                # Número de copias
                elif line_number == 27:
                    s = s.replace(
                        line, (line.replace("1,1", f"{self.copies_mumber },1"))
                    )

        self.printer_job(printer, bytes(s, "utf-8"))

    # Kids
    def print_bottle_label(self):
        printer = default_printer

        f = open(f"./printer_labels/new_bottle_{self.categoria}100ml.prn", "rb")
        s = f.read()
        f.close()

        # sex
        s = s.replace(b"X X X X X", bytes(self.sex, "utf-8"))

        # lote
        s = s.replace(b"YYYYY", bytes(f"{self.lote}", "utf-8"))

        # numero
        s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # copies number
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        self.printer_job(printer, s)

    def print_bottle_label_standard_new(self):
        printer = default_printer

        f = open(f"./labels/estandard_100ml.prn", "rb")

        s = f.read()
        f.close()

        # numero
        s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # copies number
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        self.printer_job(printer, s)

    def print_bottle_label_15ml(self):
        printer = default_printer

        if self.sex == "H O M M E":
            f = open(f"./printer_labels/new_bottle_divain15ml_homme.prn", "rb")
        else:
            f = open(f"./printer_labels/new_bottle_divain15ml.prn", "rb")

        s = f.read()
        f.close()

        # numero
        s = s.replace(b"ZZZ", bytes(f"{self.numero_divain}", "utf-8"))

        # centrar nombre
        # if self.sex == 'H O M M E':
        #   s=s.replace(b'TEXT 49,24', bytes('TEXT 49,18', 'utf-8'))

        # sex
        s = s.replace(b"X X X X X", bytes(self.sex, "utf-8"))

        # copies number
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        self.printer_job(printer, s)

    def print(self):

        tipo_ean = self.ean_botes or self.ean_muestras

        # TSC
        if self.tsc_label == "bottle":
            print("Impresora 2: BOTTLE")
            if self.categoria == "divain" and self.sex in [
                "F E M M E",
                "H O M M E",
                "U N I S E X",
                "K I D S",
            ]:
                self.print_bottle_label_standard_new()
            elif self.categoria == "solidario":
                pass
            else:
                self.print_bottle_label()

            tipo_ean = self.ean_botes
        elif self.tsc_label == "sample":
            # self.print_sample_label()
            self.print_sample_label_test()
            tipo_ean = self.ean_muestras

            print("Impresora 2: SAMPLE")

        elif self.tsc_label == "bottle15ml":
            self.print_bottle_label_15ml()

        else:

            print("Impresora 2: NINGUNA")

        # ZD
        print("Tipo EAN: ", tipo_ean)
        if self.zd_label == "box" and tipo_ean:
            self.print_box_label(tipo_ean)
            print("Impresora 1: BOX")
        else:
            print("Ipresora 1: NINGUNA")


class PrintManager:
    def __init__(self, print_data: dict, printer: Callable) -> None:
        self.copies_mumber = print_data.get("CopiesNumber", 1)
        self.printer = printer
        # self.principal_label = self.get_principal_label(print_data)
        # self.barcode_label =  self.get_barcode_label(print_data)
        self.labels_jobs = [
            ("Impresora 1", self.get_principal_label(print_data)),
            ("Impresora 2", self.get_barcode_label(print_data)),
        ]

    def get_principal_label(self, print_data: dict) -> bytes or None:
        # TODO: Implementar
        log.debug("get_principal_label - xImplementar")

        return None

    def get_barcode_label(self, print_data: dict) -> bytes or None:
        if print_data.get("zd_label", "") == "ninguna":
            return None

        printer_file = "./printer_labels/new_codigo_barras.prn"

        # TODO: Estos deben ser datos de la instancia para luego tener aparte la función de
        # parseo y reutilizzarlos en la otra etiaqueta, tal vez una dataclase referencia
        # Quien determina si vienen el bote o la muestra?
        # REvisar
        tipo_ean = print_data.get("ean_botes") or print_data.get("ean_muestras")
        sku = print_data.get("sku")

        try:
            if not tipo_ean:
                raise ValueError("No hay tipo de ean")

            # barcode
            ean_select = tipo_ean[:-1] + ">6" + tipo_ean[-1:]

            with open(printer_file, "rb") as f:
                label = f.read()

            # name
            label = label.replace(b"DIVAIN-XXX", bytes(sku, "utf-8"))

            # !105123456789012!1003
            label = label.replace(b"123456789012>63", bytes(ean_select, "utf-8"))

            # bar_print_number
            label = label.replace(b"1234567890123", bytes(tipo_ean, "utf-8"))

            # copies number
            label = label.replace(
                b"^PQ1,0,1,Y", bytes(f"^PQ{self.copies_mumber },0,1,Y", "utf-8")
            )

            return label

        except Exception as e:
            log.error(f"Error al intentar generar etiqueta de código de barra {e}")
            return None

    def print(self) -> None:
        for printer_name, label in self.labels_jobs:
            if label:
                self.printer(printer_name, label)


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
