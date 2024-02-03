import win32print

def get_printer_list():
        list=[]
        #Enum printers returns the list of printers available in the network
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_CONNECTIONS
            + win32print.PRINTER_ENUM_LOCAL)
        for printer in printers:
            list.append(printer[2])

        return list

def printer_job(printer_name, printer_file):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
      hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))  # noqa: F841
      try:
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, printer_file)
        win32print.EndPagePrinter(hPrinter)
      finally:
        win32print.EndDocPrinter(hPrinter)
    finally:
      win32print.ClosePrinter(hPrinter)

