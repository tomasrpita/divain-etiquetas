# coding: utf-8

from app.LIB.printers import printer_job


class PrinterLabels():
    def __init__(self, formdata) -> None:

       self.copies_mumber = int(formdata['CopiesNumber']) if formdata['CopiesNumber'] else 0
       self.lote = formdata['loteBotella']
       self.ean_botes = formdata['ean_botes']
       self.ean_muestras = formdata['ean_muestras']
       self.numero_divain = formdata['numero_divain']
       self.copies_mumber = formdata['CopiesNumber']
       self.sex = formdata['sexo']
       self.sku = formdata['sku']
       self.categoria = formdata['categoria']
       # self.free_sample = True if  formdata.get('free_sample') else False
       self.free_sample = formdata.get('free_sample')
       self.tsc_label = formdata['tscLabel'] if formdata['tscLabel'] != 'ninguna' else ""
       self.zd_label = formdata['zdLabel'] if formdata['zdLabel'] != 'ninguna' else ""
       


    def print_sample_label(self):
        printer = 'Impresora 1'

        # f=open("./printer_labels/new_sample_label.prn", "rb")
        
        if self.free_sample == 'free':
            if self.sex == 'H O M M E':
                f=open("./printer_labels/new_free_sample_homme.prn", "rb")
            else:
                f=open("./printer_labels/new_free_sample.prn", "rb")
                
        elif self.free_sample == 'standard':
            if self.sex == 'H O M M E':
                f=open(f"./printer_labels/new_sample_{self.categoria}_homme.prn", "rb")
            else:
                f=open(f"./printer_labels/new_sample_{self.categoria}.prn", "rb")
                
        elif self.free_sample == 'pack':
            if self.sex == 'H O M M E':
                f=open(f"./printer_labels/new_sample_{self.categoria}_pack.prn", "rb")
            else:
                f=open(f"./printer_labels/new_sample_{self.categoria}_pack.prn", "rb")
        
        s=f.read()
        f.close()

        # number
        s=s.replace(b'ZZZ', bytes(self.sku.replace('DIVAIN-', ''), 'utf-8'))

        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))

        #barcode
        ean_muestras = self.ean_muestras[:-1] + '!100' + self.ean_muestras[-1:]
        s=s.replace(b'123456789012!1003', bytes(ean_muestras, 'utf-8'))

        #copies number
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))
        
        printer_job(printer, s)
    
    


    def print_box_label(self, tipo_ean):
        printer = 'Impresora 2'
        # printer = 'ZDesigner ZD420-203dpi ZPL'

        f=open("./printer_labels/new_codigo_barras.prn", "rb")
        s=f.read()
        f.close()

        # name
        s=s.replace(b'DIVAIN-XXX', bytes(self.sku, 'utf-8'))
    
        #barcode
        ean_select = tipo_ean[:-1] + '>6' + tipo_ean[-1:]
   
        # !105123456789012!1003
        s=s.replace(b'123456789012>63', bytes(ean_select, 'utf-8'))
        
        #bar_print_number
        s=s.replace(b'1234567890123', bytes(tipo_ean, 'utf-8'))
        
        #copies number
        s=s.replace(b'^PQ1,0,1,Y', bytes(f'^PQ{self.copies_mumber },0,1,Y', 'utf-8'))
        
        
        printer_job(printer, s)


    def print_bottle_label(self):
        printer = 'Impresora 1'
        
        if self.sex == 'H O M M E':
            f=open(f"./printer_labels/new_bottle_{self.categoria}100ml_homme.prn", "rb")
        else:
            f=open(f"./printer_labels/new_bottle_{self.categoria}100ml.prn", "rb")

        # f=open(f"./printer_labels/new_bottle_divain100ml.prn", "rb")
        # f=open("./printer_labels/new_bottle_black100ml.prn", "rb")
        
        s=f.read()
        f.close()

        #centrar nombre
        #if self.sex == 'H O M M E':
        #    s=s.replace(b'TEXT 302,101', bytes('TEXT 302,95', 'utf-8'))

        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))
    
        #lote
        s=s.replace(b'YYYYY', bytes(f'{self.lote}', 'utf-8'))
        
        #numero
        s=s.replace(b'ZZZ', bytes(self.sku.replace('DIVAIN-', ''), 'utf-8'))

        #copies number
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))

        printer_job(printer, s)
        
    def print_bottle_label_15ml(self):
        printer = 'Impresora 1'
        
        
        if self.sex == 'H O M M E':
            f=open(f"./printer_labels/new_bottle_divain15ml_homme.prn", "rb")
        else:
            f=open(f"./printer_labels/new_bottle_divain15ml.prn", "rb")


        
        s=f.read()
        f.close()

        
        #numero
        s=s.replace(b'ZZZ', bytes(f'{self.numero_divain}', 'utf-8'))
        
        #centrar nombre
        #if self.sex == 'H O M M E':
        #   s=s.replace(b'TEXT 49,24', bytes('TEXT 49,18', 'utf-8'))
        
        #sex
        s=s.replace(b'X X X X X', bytes(self.sex, 'utf-8'))

        #copies number
        s=s.replace(b'PRINT 1,1', bytes(f'PRINT {self.copies_mumber },1', 'utf-8'))

        printer_job(printer, s) 

    def print(self):
    
        tipo_ean = self.ean_botes or  self.ean_muestras

        # TSC
        if self.tsc_label == 'bottle':
            self.print_bottle_label()
            print("TSC: BOTTLE")
            tipo_ean = self.ean_botes
        elif self.tsc_label == 'sample':
            self.print_sample_label()
            tipo_ean = self.ean_muestras
            
            print("TSC: SAMPLE")
        elif self.tsc_label == 'bottle15ml':
            self.print_bottle_label_15ml()
            
        else:
            print("TSC: NINGUNA")

        # ZD
        print("Tipo EAN: ", tipo_ean)
        if self.zd_label == 'box' and tipo_ean:
            self.print_box_label(tipo_ean)
            print("TSC: BOX")
        else:
            print("TSC: NINGUNA")