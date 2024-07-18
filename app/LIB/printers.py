import win32print
import win32api

def printer_job(printer_name, printer_file):
    print(f"Intentando imprimir en: {printer_name}")
    print(f"Tamaño de los datos a imprimir: {len(printer_file)} bytes")
    
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        print("Impresora abierta con éxito")
    except Exception as e:
        print(f"Error al abrir la impresora: {e}")
        return

    try:
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))
            print(f"Trabajo de impresión iniciado: {hJob}")
        except Exception as e:
            print(f"Error al iniciar el trabajo de impresión: {e}")
            return

        try:
            win32print.StartPagePrinter(hPrinter)
            print("Página de impresión iniciada")
            
            bytes_written = win32print.WritePrinter(hPrinter, printer_file)
            print(f"Bytes escritos en la impresora: {bytes_written}")
            
            if bytes_written != len(printer_file):
                print("ADVERTENCIA: No se escribieron todos los bytes")
            
            win32print.EndPagePrinter(hPrinter)
            print("Página de impresión finalizada")
        except Exception as e:
            print(f"Error durante la impresión: {e}")
        finally:
            win32print.EndDocPrinter(hPrinter)
            print("Documento de impresión finalizado")
    finally:
        win32print.ClosePrinter(hPrinter)
        print("Impresora cerrada")

    print("Trabajo de impresión completado")
