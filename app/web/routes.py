# coding: utf-8

import os
from app.LIB.print_labels import PrinterLabels
from app.services.labels_info_service import get_labels_info
from flask import render_template, flash, request, abort, current_app
from app.LIB.utils import get_copies_number
from app.web import bp

def fake_printer_job(printer_name, printer_file):
	log.info(f"Fake printer job printer name: {printer_name}")
	log.info(f"Fake printer job printer_file: {printer_file}")


# check if os is windows or mac
if os.name == "nt":
	# windows
	from app.LIB.printers import printer_job
	on_production = True
	printers = printer_job
	# printers = fake_printer_job
	api_prodruction_order = current_app.config["BASE_URL"] + current_app.config["PRODUCTION_ORDER_URL"]
else:
	# mac
	printers = fake_printer_job
	on_production = False
	api_prodruction_order = "http://127.0.0.1:8000/" + current_app.config["PRODUCTION_ORDER_URL"]


log = current_app.logger

# get labels info
labels_info, error = get_labels_info(on_production)


@bp.route("/", methods=["GET", "POST"])
@bp.route("/home", methods=["GET", "POST"])
def home():

	formdata = None

	if request.method == "POST":
		formdata = request.form.to_dict(flat=True)
		PrinterLabels(formdata, printers).print()

		copies_number = request.form.get("CopiesNumber")

	else:
		if error or not labels_info:
			error_message =  error or "Datos vienen vacios."
			flash(f"Error tratando de obtener los datos de las etiquetas: {error_message}", "danger")
			abort(404)


		copies_number = get_copies_number()

	return render_template(
		"tpt_form_print_labels.html",
		form_action="web.home",
		copies_number=copies_number,
		formdata=formdata,
		labels_info=labels_info,
	)


@bp.route("/pro", methods=["GET"])
def pro_labels():

	if error or not labels_info:
			error_message =  error or "Datos vienen vacios."
			flash(f"Error tratando de obtener los datos de las etiquetas: {error_message}", "danger")
			abort(404)


	return render_template(
		"tpt_form_print_labels_pro.html",
		form_action="web.pro_labels",
		labels_info=labels_info,
		api_prodruction_order=api_prodruction_order
	)


@bp.route("/pro/print", methods=["POST"])
def pro_print_labels():

	# get form data from json
	formdata = request.get_json()

	# check batch is present
	if not formdata.get("batch"):
		return {
			"status": "error",
			"message": "No se ha enviado el numero de lote."
		}
	
	PrinterLabels(formdata, printers).print()

	return {
		"status": "ok",
		"printed": True
	}