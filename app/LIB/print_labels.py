from app.LIB.printers import printer_job
import os
import re

class PrinterLabels:
    def __init__(self, formdata) -> None:
        self.copies_mumber = int(formdata["CopiesNumber"]) if formdata["CopiesNumber"] else 0
        self.lote = formdata["loteBotella"]
        self.ean_botes = formdata["ean_botes"]
        self.ean_muestras = formdata["ean_muestras"]
        self.numero_divain = formdata["numero_divain"]
        self.sex = formdata["sexo"]
        self.sku = formdata["sku"]
        self.categoria = formdata["categoria"]
        self.free_sample = formdata.get("free_sample")
        self.tsc_label = formdata["tscLabel"] if formdata["tscLabel"] != "ninguna" else ""
        self.zd_label = formdata["zdLabel"] if formdata["zdLabel"] != "ninguna" else ""

    def print_sample_label(self):
        printer = "Impresora 1"
        divain_number = self.sku.replace("DIVAIN-", "")

        # Determina el archivo PRN a utilizar basado en la lógica existente
        if len(divain_number) == 4:
            file_name = "./printer_labels/new_sample_0000_UNISEX_divain.prn"
        elif self.free_sample == "free":
            file_name = "./printer_labels/new_free_sample_homme.prn" if self.sex == "H O M M E" else "./printer_labels/new_free_sample.prn"
        elif self.free_sample == "standard":
            file_name = f"./printer_labels/new_free_sample_homme.prn" if self.sex == "H O M M E" else f"./printer_labels/new_free_sample_homme.prn"
        elif self.free_sample == "pack":
            file_name = f"./printer_labels/new_sample_{self.categoria}_pack.prn" if self.sex == "H O M M E" else f"./printer_labels/new_sample_{self.categoria}_pack.prn"
        else:
            raise ValueError("Tipo de muestra desconocido")

        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"El archivo {file_name} no se encuentra en la ruta especificada.")

        with open(file_name, "rb") as f:
            prn_data = f.read()

        # Reemplazar placeholders
        prn_data = prn_data.replace(b"ZZZ", bytes(divain_number, "utf-8"))
        prn_data = prn_data.replace(b"XXXXX", bytes(self.sex, "utf-8"))
        prn_data = prn_data.replace(b"123456789012", bytes(self.ean_muestras, "utf-8"))

        # Reemplazar el número de copias
        prn_data = re.sub(rb"\^PQ\d+", bytes(f"^PQ{self.copies_mumber}", "utf-8"), prn_data)

       
        # Imprimir los datos
        printer_job(printer, prn_data)

    def print_box_label(self, tipo_ean):
        printer = "Impresora 2"
        file_name = "./printer_labels/new_codigo_barras.prn"

        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"El archivo {file_name} no se encuentra en la ruta especificada.")

        with open(file_name, "rb") as f:
            prn_data = f.read()

        # Reemplazar placeholders
        if re.match(r"DIVAIN-DS[0-9A-Za-z]{2}$", self.sku):
            self.sku = self.sku.replace("-", "")

        prn_data = prn_data.replace(b"DIVAIN-XXX", bytes(self.sku, "utf-8"))
        ean_select = tipo_ean[:-1] + ">6" + tipo_ean[-1:]
        prn_data = prn_data.replace(b"123456789012>63", bytes(ean_select, "utf-8"))
        prn_data = prn_data.replace(b"1234567890123", bytes(tipo_ean, "utf-8"))
        prn_data = prn_data.replace(b"^PQ1,0,1,Y", bytes(f"^PQ{self.copies_mumber},0,1,Y", "utf-8"))


        # Imprimir los datos
        printer_job(printer, prn_data)

    def print(self):
        tipo_ean = self.ean_botes or self.ean_muestras

        # TSC
        if self.tsc_label == "bottle":
            self.print_bottle_label()
            print("TSC: BOTTLE")
            tipo_ean = self.ean_botes
        elif self.tsc_label == "sample":
            self.print_sample_label()
            tipo_ean = self.ean_muestras
            print("TSC: SAMPLE")
        elif self.tsc_label == "bottle15ml":
            self.print_bottle_label_15ml()
        else:
            print("TSC: NINGUNA")

        # ZD
        if self.zd_label == "box" and tipo_ean:
            self.print_box_label(tipo_ean)
        else:
            print("TSC: NINGUNA")

