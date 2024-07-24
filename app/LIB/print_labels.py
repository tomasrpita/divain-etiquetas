# coding: utf-8

# from app.LIB.printers import printer_job
import os
from dataclasses import dataclass
import logging
from typing import Callable, List
from app.LIB.utils import get_printers
import json

log = logging.getLogger(__name__)
default_printer, codebar_printer, black_printer = get_printers()

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


# TODO Si hay mas de 15 lineas de ingredientes avisar que no se puede imprimir
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
        # self.free_sample = True if  formdata.get('free_sample') else False
        self.free_sample = formdata.get("free_sample")
        self.tsc_label = (
            formdata["tscLabel"] if formdata["tscLabel"] != "ninguna" else ""
        )

        self.zd_label = formdata.get("zdLabel")
        self.fragance_name  = formdata.get("fragance_name")

        # GRupo de etiquetas destino
        self.label_destination = formdata.get("label_destination")
        self.printer_job = printer_job
        self.pro = pro

        self.fecha = self.extract_date_from_ean(formdata["eanBotella"])

        print(formdata)

    def extract_date_from_ean(self, ean):
        # Buscar el código de fecha que sigue a ')17='
        try:	
            date_code = ean.split(')17=')[1][:6]  # Los primeros 6 caracteres después de ')17='
            return date_code
        except IndexError:
            # Manejar el caso donde no se encuentra la fecha o el formato es incorrecto
            print("Formato de fecha incorrecto o inexistente en eanBotella.")
            return None

    def print_sample_label_test(self):
        printer = default_printer
        print("Sample:", default_printer)

        f = open("./printer_labels/new_sample_label_test.prn", "rb")

        # f=open("./printer_labels/new_sample_label.prn", "rb")
        s = f.read()
        f.close()

        self.ean_13 = self.ean_muestras or self.ean_botes

        # number
        s = s.replace(b"XXX", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # sex
        s = s.replace(b"X X X X X", bytes(self.sex, "utf-8"))

        # barcode
        ean_13 = self.ean_13[:-1] + "!100" + self.ean_13[-1:]
        s = s.replace(b"123456789012!1003", bytes(ean_13, "utf-8"))

        # copies number
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        self.printer_job(printer, s)

    # TODO: Not currently in Use
    def print_sample_label(self):
        printer = default_printer
        print("Sample:", default_printer)

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

    # TODO: Not currently in Use
    def print_box_label(self, tipo_ean):
        printer = codebar_printer
        print("Box:", codebar_printer)
        # printer = 'ZDesigner ZD420-203dpi ZPL'

        f = open("./labels/codigo_barras_ingredientes_usa.prn", "r")
        s = f.read()
        f.close()

        line_length = 20
        lista_ingredientes = split_text(self.ingredientes, line_length)
        # print('Número de lineas de ingredientes: ', len(liskta_ingredientes))
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
                                    "XXXXXXXXXXXXXXXXX",
                                    lista_ingredientes[line_number - 12],
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
        print("Bottle:", default_printer)

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
        if (self.sex == "H O M M E" or self.categoria == "black") and self.categoria != "ken":
            printer = black_printer
        elif self.sex == "U N I S E X" and (("001" <= self.numero_divain <= "049") or ("200" <= self.numero_divain <= "499")):
            printer = black_printer
        else:
            printer = default_printer

        print("Bottle:", self.sku, self.categoria)

        if self.fragance_name == 'HOPE':
            label_file = "./labels/nueva-home-hope.prn"
        elif self.fragance_name == 'REBEL':
            label_file = "./labels/nueva-home-rebel.prn"
        elif self.fragance_name == 'FEELING':
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
        elif self.categoria == 'oriental':
            label_file = "./labels/nueva-zzzz-oriental.prn"
        elif self.categoria == 'ken':
            label_file = "./labels/nueva-ken.prn"
        elif self.categoria == 'barbie':
            label_file = "./labels/nueva-barbie.prn"
        elif self.categoria == "black":
            label_file = "./labels/nueva-black.prn"
        elif self.sex == "K I D S":
            label_file = "./labels/nueva-kids.prn"
        else:
            label_file = "./labels/nueva.prn"

        # Abre el archivo PRN que contiene la plantilla de la etiqueta.
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
        
    
        # Reemplaza "ZZZ" con el número SKU, excluyendo el prefijo "DIVAIN-".
        s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # Reemplaza "XXX" con el valor de sexo correspondiente.
        s = s.replace(b"for XXX", bytes(sex_text, "utf-8"))

        # Corrección en el nombre de la variable para número de copias
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber},1", "utf-8"))

        # Imprime el contenido final que se enviará a la impresora para depuración
        try:
            print_content = s.decode('utf-8')
            print("Contenido enviado a la impresora:")
        except UnicodeDecodeError:
            print("Contenido en bytes; no se puede mostrar como texto.")

        # Envía la cadena modificada para impresión.
        self.printer_job(printer, s)

    # in testing phase
    def print_qr_label(self):
        printer = default_printer
        print("QR:", default_printer)

        f = open(f"./labels/estandard_{self.tsc_label}_100ml.prn", "rb")

        s = f.read()
        f.close()

        # numero
        s = s.replace(b"ZZZ", bytes(self.sku.replace("DIVAIN-", ""), "utf-8"))

        # copies number
        s = s.replace(b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8"))

        self.printer_job(printer, s)

    def print_bottle_label_15ml(self):
        printer = default_printer
        print("Bottle:", default_printer)

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

    def print_destination_group_label(self, labels_info: dict):
        printer = codebar_printer

        base_dir = "./labels/"

        # Workaround for change number of copies
        self.copies_mumber = 45 if self.pro else self.copies_mumber

        if labels_info["destination"] == "MX":
            f = open(os.path.join(base_dir, labels_info["file"]), "rb")
            s = f.read()
            f.close()

            # Lote bottle
            s = s.replace(b"XXXXXX", bytes(f"{self.lote}", "utf-8"))

            # # SKU box
            s = s.replace(b"DIVAIN-ZZZ", bytes(f"{self.sku}", "utf-8"))

            # # Lote box
            # s = s.replace(b"LLLLLLLLLLL", bytes(f"{self.lote}", "utf-8"))
            s = s.replace(b"xxxxxxxxxx", bytes(f"{self.lote}", "utf-8"))

            # bar code
            ean_select = self.ean_botes[:-1] + "!100" + self.ean_botes[-1:]
            s = s.replace(b"123456789012!1003", bytes(ean_select, "utf-8"))

            # ean number
            s = s.replace(b"1234567890123", bytes(f"{self.ean_botes}", "utf-8"))

            # Copies number
            s = s.replace(
                b"PRINT 1,1", bytes(f"PRINT {self.copies_mumber },1", "utf-8")
            )

            qr_data = f"(01){self.ean_botes}(10){self.lote}(17){self.fecha}"
            qr_bytes = bytes(qr_data, 'utf-8')
            s = s.replace(b"YYYY", qr_bytes)

        else:
            f = open(os.path.join(base_dir, labels_info["file"]), "rb")
            s = f.read()
            f.close()

            line_length = 30
            lista_ingredientes = split_text(self.ingredientes, line_length)

            with open(os.path.join(base_dir, labels_info["file"]), "rb") as f:
                for line_number, line in enumerate(f, start=1):
                    # SKU
                    # lista de ingredientes
                    if (
                        labels_info["ingredient_lines"]["start"]
                        <= line_number
                        <= labels_info["ingredient_lines"]["end"]
                    ):
                        index = line_number - labels_info["ingredient_lines"]["start"]
                        print(index)
                        # print(lista_ingredientes[index - 1])
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
                        # SKU box
                        s = s.replace(
                            line,
                            (line.replace(b"DIVAIN-ZZZ", bytes(self.sku, "utf-8"))),
                        )

                    elif line_number == labels_info["barcode_box_line"]:
                        # Codebar box
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
                        # Ean box
                        s = s.replace(
                            line,
                            (
                                line.replace(
                                    b"1234567890123", bytes(self.ean_botes, "utf-8")
                                )
                            ),
                        )

                    elif line_number == labels_info["lote_box_line"]:
                        # Lote box
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
                        qr_bytes = bytes(qr_data, 'utf-8')
                        s = s.replace(line, line.replace(b"YYYY", qr_bytes))

        self.printer_job(printer, s)

    def print(self):
        tipo_ean = self.ean_botes or self.ean_muestras

        avoid_print_bottle_skus = [
        
            
        ]

        # Bloque que se relaciona con lo marcado en le formulario como impresora 1

        if self.sku.endswith(tuple(avoid_print_bottle_skus)):
            pass

        elif self.tsc_label == "bottle":
            if self.categoria == "divain" or "home" and self.sex in [
                "F E M M E",
                "H O M M E",
                "U N I S E X",
                "K I D S",
                "H O M E",
            ]:
                self.print_bottle_label_standard_new()

            # Son preimpresas no se imprimen
            elif self.sex == "H O M E":
                pass

            elif self.categoria == "solidario":
                pass
            else:
                self.print_bottle_label()

            tipo_ean = self.ean_botes
        elif self.tsc_label == "sample":
            self.print_sample_label_test()
            tipo_ean = self.ean_muestras

        elif self.tsc_label == "QR_HQ" or self.tsc_label == "QR_QQ":
            self.print_qr_label()

        # elif self.tsc_label == "sample":

        # print("Impresora 2: SAMPLE")

        elif self.tsc_label == "bottle15ml":
            self.print_bottle_label_15ml()

        else:
            print("Ninguna: ", default_printer)

        # Bloque que se relaciona con lo marcado en le formulario como impresora 2
        if self.zd_label == "destination_group":
            # Destinos UE UK USA MX
            if self.label_destination in destinations.keys():
                self.print_destination_group_label(destinations[self.label_destination])
            else:
                log.error("Destino no válido")

        # if self.zd_label == "box" and tipo_ean:
        #     # self.print_box_label(tipo_ean)
        else:
            print("Ninguna: ", codebar_printer)


# An idea for a new label printing manager
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
