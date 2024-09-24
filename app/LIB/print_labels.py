# coding: utf-8

# from app.LIB.printers import printer_job
import os
from dataclasses import dataclass
import logging
from typing import Callable, List
from app.LIB.utils import get_printers
import json
import random
import string

log = logging.getLogger(__name__)
default_printer, codebar_printer, black_printer = get_printers()

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
        "file": "ue-bottle-box-codebar-sato.prn",
        "QR_box_line": 36,
    },
    "UK": {
        "destination": "UK",
        "ingredient_lines": {
            "start": 25,
            "end": 34,
        },
        "lote_bottle_line": 15,
        "lote_box_line": 36,
        "sku_box_line": 35,
        "barcode_box_line": 37,
        "ean_box_line": 38,
        "copies_number_line": 39,
        "file": "uk-bottle-box-codebar-sato.prn",
        "QR_box_line": 24,
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
        "file": "usa-bottle-box-codebar-sato.prn",
        "QR_box_line": 35,
    },
    "MX": {
        "destination": "MX",
        "ingredient_lines": {
            "start": 0,
            "end": 0,
        },
        "lote_bottle_line": 21,  # for no print
        "lote_box_line": 41,
        "sku_box_line": 40,
        "barcode_box_line": 42,
        "ean_box_line": 43,
        "copies_number_line": 44,
        "file": "mx-bottle-box-codebar-sato.prn",
        "QR_box_line": 31,

    },
}


def generar_codigo_serie():
    # La primera letra es siempre 'A'
    primera_letra = "A"
    
    # Las dos letras siguientes son aleatorias entre 'A' y 'Z'
    letras_aleatorias = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    # Retorna el código en formato AXX
    return primera_letra + letras_aleatorias

def generar_codigo_reimpresion():
    # La primera letra es siempre 'R'
    primera_letra = "R"
    
    # Las dos letras siguientes son aleatorias entre 'A' y 'Z'
    letras_aleatorias = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    # Retorna el código en formato AXX
    return primera_letra + letras_aleatorias

def generar_codigo_devolución():
    # La primera letra es siempre 'D'
    primera_letra = "D"
    
    # Las dos letras siguientes son aleatorias entre 'A' y 'Z'
    letras_aleatorias = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    # Retorna el código en formato AXX
    return primera_letra + letras_aleatorias

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
        self.fragance_name  = formdata.get("fragance_name")
        self.label_destination = formdata.get("label_destination")
        self.printer_job = printer_job
        self.pro = pro

        self.formdata = formdata
        self.is_home = formdata.get("isHome") == 'true'  
        self.is_pro = formdata.get("isPro") == 'true'

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
        s = s.replace(b"^PQ1", bytes(f"^PQ{self.copies_mumber}", "utf-8"))

        try:
            print_content = s.decode('utf-8')
            print("Contenido enviado a la impresora:")
        except UnicodeDecodeError:
            print("Contenido en bytes; no se puede mostrar como texto.")

        # Envía la cadena modificada para impresión.
        self.printer_job(printer, s)
    
    def print_destination_group_label(self, labels_info: dict, formData: dict):
        labels_info = labels_info.copy()
    
        if labels_info["destination"] == "UE" and self.sex == "H O M E":
            labels_info["file"] = "ue-bottle-box-codebar-home-sato.prn"

        printer = codebar_printer
        base_dir = "./labels/"
        print("formdata", self.formdata)

        # Aseguramos que si es Pro se imprimen 50 copias
        self.copies_mumber = 50 if self.formdata.get('isPro', False) else int(self.copies_mumber)

        generated_codes = set()

        # Bucle para generar el código y mandar a imprimir tantas veces como copias
        for copy in range(self.copies_mumber):
            # Generar un nuevo código de lote o reimpresión según corresponda
            while True:
                if self.formdata.get('isPro', False):
                    # Si viene de /pro, generamos el código de lote aleatorio
                    codigo_lote = generar_codigo_serie()
                elif self.formdata.get('isHome', False):
                    # Si viene de /home, generamos el código de reimpresión
                    codigo_lote = generar_codigo_reimpresion()
                else:
                    print("No viene ni de home ni de pro")
                    return

                # Verificar que el código sea único en esta impresión
                if codigo_lote not in generated_codes:
                    generated_codes.add(codigo_lote)
                    break
                else:
                    print(f"Código duplicado detectado: {codigo_lote}, generando uno nuevo...")

            # Leer el archivo de plantilla en cada iteración para asegurarse de que está limpio en cada copia
            with open(os.path.join(base_dir, labels_info["file"]), "rb") as f:
                s = f.read()

            line_length = 30
            lista_ingredientes = split_text(self.ingredientes, line_length)

            # Procesar y reemplazar líneas en la plantilla
            lines = s.split(b'\n')
            for line_number, line in enumerate(lines, start=1):
                if (
                    "ingredient_lines" in labels_info and
                    labels_info["ingredient_lines"]["start"] <= line_number <= labels_info["ingredient_lines"]["end"]
                ):
                    index = line_number - labels_info["ingredient_lines"]["start"]
                    if index_exists(lista_ingredientes, index):
                        lines[line_number - 1] = line.replace(
                            b"####################",
                            bytes(lista_ingredientes[index], "utf-8")
                        )
                    else:
                        lines[line_number - 1] = b""
                elif line_number == labels_info.get("lote_bottle_line"):
                    lines[line_number - 1] = line.replace(b"XXXXXX", bytes(self.lote, "utf-8"))
                elif line_number == labels_info.get("sku_box_line"):
                    lines[line_number - 1] = line.replace(b"DIVAIN-ZZZ", bytes(self.sku, "utf-8"))
                elif line_number == labels_info.get("barcode_box_line"):
                    ean_select = self.ean_botes
                    lines[line_number - 1] = line.replace(b"123456789012", bytes(ean_select, "utf-8"))
                elif line_number == labels_info.get("ean_box_line"):
                    lines[line_number - 1] = line.replace(b"123456789012", bytes(self.ean_botes, "utf-8"))
                elif line_number == labels_info.get("lote_box_line"):
                    lines[line_number - 1] = line.replace(b"xxxxxxxxxx", bytes(self.lote, "utf-8"))
                elif line_number == labels_info.get("copies_number_line"):
                    # Configuramos para imprimir solo una copia por vez
                    lines[line_number - 1] = line.replace(b"1,1", b"1,1")
                    lines[line_number - 1] = lines[line_number - 1].replace(b"^PQ1", b"^PQ1")
                elif line_number == labels_info.get("QR_box_line"):
                    qr_data = f"((((01)1{self.ean_botes}(10){self.lote}(21){codigo_lote}"
                    qr_bytes = qr_data.encode('utf-8')
                    lines[line_number - 1] = line.replace(b"YYYY", qr_bytes)

            # Reconstruir la plantilla modificada
            s = b'\n'.join(lines)

            # Enviar a imprimir en cada iteración con el código generado
            print(f"Enviando impresión {copy + 1}/{self.copies_mumber} con código {codigo_lote}")
            self.printer_job(printer, s)  # Aquí se envía la impresión por cada copia con su código

    def print(self):
        tipo_ean = self.ean_botes or self.ean_muestras

        avoid_print_bottle_skus = []

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
        elif self.tsc_label == "bottle15ml":
            self.print_bottle_label_15ml()
        else:
            print("Ninguna: ", default_printer)

        # Bloque que se relaciona con lo marcado en le formulario como impresora 2
        if self.zd_label == "destination_group":
            # Destinos UE UK USA MX
            if self.label_destination in destinations.keys():
                self.print_destination_group_label(destinations[self.label_destination], self.formdata)
            else:
                log.error("Destino no válido")
        else:
            print("Ninguna: ", codebar_printer)

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
