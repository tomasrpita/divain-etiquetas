# coding: utf-8

from app.LIB.printers import printer_job


class PrinterLabels():
    def __init__(self, formdata) -> None:

       self.copies_mumber = int(formdata['CopiesNumber']) if formdata['CopiesNumber'] else 0
       self.lote = formdata['loteBotella']
       self.ean_13 = formdata['ean_13']
       self.numero_divain = formdata['numero_divain']
       self.copies_mumber = formdata['CopiesNumber']
       self.sex = formdata['sexo']
       self.sku = formdata['sku']
       self.tsc_label = formdata['tscLabel'] if formdata['tscLabel'] != 'ninguna' else ""
       self.zd_label = formdata['zdLabel'] if formdata['zdLabel'] != 'ninguna' else ""
       


    def print_sample_label(self):
        printer = 'Impresora 1'

        f=open("./printer_labels/new_sample_label.prn", "rb")
        s=f.read()
        f.close()

        # number
        s=s.replace(b'XXX', bytes(self.sku.replace('DIVAIN-', ''), 'utf-8'))

        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))

        #barcode
        ean_13 = self.ean_13[:-1] + '!100' + self.ean_13[-1:]
        s=s.replace(b'123456789012!1003', bytes(ean_13, 'utf-8'))

        #copies number
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))
        
        printer_job(printer, s)


    def print_box_label(self):
        printer = 'Impresora 2'
        # printer = 'ZDesigner ZD420-203dpi ZPL'

        f=open("./printer_labels/new_box_label.prn", "rb")
        s=f.read()
        f.close()

        # name
        s=s.replace(b'DIVAIN-XXX', bytes(self.sku, 'utf-8'))
    
        #barcode
        # ean_13 = self.ean_13[:-1] + '>6' + self.ean_13[-1:]
        ean_13 = self.ean_13[:-1] + '!100' + self.ean_13[-1:]
        # !105123456789012!1003
        # s=s.replace(b'123456789012>63', bytes(ean_13, 'utf-8'))
        s=s.replace(b'123456789012!1003', bytes(ean_13, 'utf-8'))
        #bar_print_number
        s=s.replace(b'1234567890123', bytes(self.ean_13, 'utf-8'))
        #copies number
        # s=s.replace(b'^PQ1,0,1,Y', bytes(f'^PQ{self.copies_mumber },0,1,Y', 'utf-8'))
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))
        printer_job(printer, s)


    def print_bottle_label(self):
        printer = 'Impresora 1'

        f=open("./printer_labels/new_bottle_label.prn", "rb")
        s=f.read()
        f.close()

        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))
    
        #lote
        s=s.replace(b'YYYYY', bytes(f'{self.lote}', 'utf-8'))
        
        #numero
        s=s.replace(b'ZZZ', bytes(self.sku.replace('DIVAIN-', ''), 'utf-8'))

        #copies number
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))

        printer_job(printer, s)

    def print(self):

        # TSC
        if self.tsc_label == 'bottle':
            self.print_bottle_label()
            print("TSC: BOTTLE")
        elif self.tsc_label == 'sample':
            self.print_sample_label()
            print("TSC: SAMPLE")
        else:
            print("TSC: NINGUNA")

        # ZD
        if self.zd_label == 'box':
            self.print_box_label()
            print("TSC: BOX")
        else:
            print("TSC: NINGUNA")
