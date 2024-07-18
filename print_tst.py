import win32print
import os

def list_printers():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    for printer in printers:
        print(printer[2])

def printer_job(printer_name, file_path):
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        print(f"Impresora {printer_name} abierta.")
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Test Print", None, "RAW"))
            print(f"Documento de impresión iniciado.")
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                print(f"Datos leídos del archivo: {data}")  # Verificar los datos leídos
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, data)
                win32print.EndPagePrinter(hPrinter)
                print(f"Página de impresión finalizada.")
            except Exception as e:
                print(f"Error al escribir en la impresora: {e}")
            finally:
                win32print.EndDocPrinter(hPrinter)
                print(f"Documento de impresión finalizado.")
        except Exception as e:
            print(f"Error al iniciar el documento de impresión: {e}")
        finally:
            win32print.ClosePrinter(hPrinter)
            print(f"Impresora {printer_name} cerrada.")
    except Exception as e:
        print(f"Error al abrir la impresora: {e}")

# Comandos SZPL básicos para una impresora SATO CL4NX Plus
prn_data = b"""
^XA
^CW1,E:ARIAL.TTF
^PW944
^LL832
^MD11
^PR8
^FO70,90^A1R,44,44^FDXXXXX^FS
^FO140,110^GB4,150,4^FS    
^FO135,125^A1R,80,80^FDZZZ^FS 
^PQ5
^XZ
"""

file_path = "etiqueta_sato.prn"
with open(file_path, "wb") as file:
    file.write(prn_data)

# Verificar que el archivo ha sido creado y leer su contenido
if os.path.exists(file_path):
    print(f"Archivo {file_path} creado con éxito.")
    with open(file_path, "rb") as file:
        content = file.read()
        print(f"Contenido del archivo: {content}")
else:
    print(f"Error: El archivo {file_path} no se ha creado.")

# Nombre de la impresora
printer_name = "Impresora 1"  # Asegúrate de que este nombre coincide con el nombre real de tu impresora

# Verificar y listar impresoras disponibles
print("Impresoras disponibles:")
list_printers()

# Enviar el archivo de impresión
print("Enviando el trabajo de impresión...")
printer_job(printer_name, file_path)
print("Trabajo de impresión enviado.")
