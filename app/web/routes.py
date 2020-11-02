# coding: utf-8

from flask import render_template, flash, request, redirect, url_for
from flask import current_app

from app.LIB.utils import get_copies_number

from app.web import bp

log = current_app.logger

@bp.route("/")
@bp.route("/home")
def home():

    copies_number = get_copies_number()




    return render_template("tpt_form_print_labels.html", form_action="web.home", copies_number=copies_number)

