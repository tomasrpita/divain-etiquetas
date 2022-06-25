# coding: utf-8

from app.LIB.print_labels import PrintManager, PrinterLabels
from flask import render_template, flash, request, redirect, url_for
from flask import current_app
# from app.LIB.printers import printer_job


from app.LIB.utils import get_copies_number

from app.web import bp

log = current_app.logger

def fake_printer_job(printer_name, printer_file):
    log.info(f"Fake printer job printer name: {printer_name}")
    log.info(f"Fake printer job printer_file: {printer_file}")

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/home", methods=['GET', 'POST'])
def home():


    formdata = None

    copies_number = get_copies_number()

    if request.method == 'POST':
        formdata = request.form.to_dict(flat=True)
        # if formdata['loteBotella']:
        # PrinterLabels(formdata, printer_job).print()
        # PrinterLabels(formdata, printer_job).print()
        # PrinterLabels(formdata, fake_printer_job).print()
        PrintManager(formdata, fake_printer_job).print()

        copies_number = request.form.get('CopiesNumber')


    return render_template("tpt_form_print_labels.html", form_action="web.home", copies_number=copies_number, formdata=formdata)

