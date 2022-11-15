# coding: utf-8

import os
from app.LIB.print_labels import PrintManager, PrinterLabels, ReferenceLabelData
from flask import render_template, flash, request, redirect, url_for, abort, current_app
from app.LIB.utils import get_database_name

from app.LIB.printers import printer_job


from app.LIB.utils import get_copies_number

from app.web import bp

log = current_app.logger

database_name = get_database_name()


def fake_printer_job(printer_name, printer_file):
	log.info(f"Fake printer job printer name: {printer_name}")
	log.info(f"Fake printer job printer_file: {printer_file}")


def database_exists(name):
	path = os.path.join(os.getcwd(), "database", name)
	return os.path.isfile(path)


@bp.route("/", methods=["GET", "POST"])
@bp.route("/home", methods=["GET", "POST"])
def home():

	formdata = None

	if request.method == "POST":
		formdata = request.form.to_dict(flat=True)
		# PrinterLabels(formdata, fake_printer_job).print()
		PrintManager(formdata, printer_job).print()

		copies_number = request.form.get("CopiesNumber")

	else:
		if not database_exists(database_name):
			flash("No encontrada fichero de base de datos {database_name}", "danger")
			abort(404)

		copies_number = get_copies_number()

	return render_template(
		"tpt_form_print_labels.html",
		form_action="web.home",
		copies_number=copies_number,
		formdata=formdata,
	)
