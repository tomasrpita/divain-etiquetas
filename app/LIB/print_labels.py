# coding: utf-8

from app.LIB.printers import printer_job


class PrinterLabels():
    def __init__(self, formdata) -> None:

       self.copies_mumber = formdata['CopiesNumber']
       self.loteBotella = formdata['loteBotella']
       self.ean_13 = formdata['ean_13']
       self.numero_divain = formdata['numero_divain']
       self.copies_mumber = formdata['CopiesNumber']
       self.sex = formdata['sexo']
       self.sku = formdata['sku']
       


    def print_sample_label(self):
        printer = 'TSC TTP-345'

        f=open("./printer_labels/sample_label.prn", "rb")
        s=f.read()
        f.close()

        # number
        s=s.replace(b'XXX', bytes(self.sku.replace('DIVAIN-', ''), 'utf-8'))

        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))

        #barcode
        ean_13 = self.ean_13[:-1] + '!100' + self.ean_13[-1:]
        s=s.replace(b'123456789012!1003', bytes(ean_13, 'utf-8'))

    def print_box_label(self):
        printer = 'ZDesigner ZD420-203dpi ZPL'

        f=open("./printer_labels/box_label.prn", "rb")
        s=f.read()
        f.close()

        # name
        s=s.replace(b'DIVAIN-001', b'DIVAIN-666')
    
        #ean13
        test_divain_ean_13 = test_divain_ean_13[:-1] + '>6' + test_divain_ean_13[-1:]
        s=s.replace(b'123456789012>63', bytes(test_divain_ean_13, 'utf-8'))





        printer_job(printer, s)

