# coding: utf-8

from app.LIB.print_labels import PrinterLabels
from flask import render_template, flash, request, redirect, url_for
from flask import current_app

from app.LIB.utils import get_copies_number

from app.web import bp

log = current_app.logger

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/home", methods=['GET', 'POST'])
def home():

    copies_number = get_copies_number()

    if request.method == 'POST':
        formdata = request.form.to_dict(flat=True)
        if formdata['loteBotella']:
            PrinterLabels(formdata).print()
        return redirect(url_for('web.home'))

    return render_template("tpt_form_print_labels.html", form_action="web.home", copies_number=copies_number)

