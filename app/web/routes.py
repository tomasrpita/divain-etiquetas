# coding: utf-8

from flask import render_template, flash, request, redirect, url_for
from flask import current_app

from app.web import bp

log = current_app.logger

@bp.route("/")
@bp.route("/home")
def home():


    return render_template("tpt_base.html", current_page="home")

