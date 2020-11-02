# coding: utf-8
"Vistas que manejan errores"
from flask import render_template
from flask import current_app
from app.errors import bp
from flask import request


@bp.app_errorhandler(400)
def error400(error):
    current_app.logger.error(error)
    return render_template("errors/400.html"), 400


@bp.app_errorhandler(401)
def error401(error):
    current_app.logger.error(error)
    return render_template("errors/401.html"), 401


@bp.app_errorhandler(403)
def error403(error):
    current_app.logger.error(error)
    return render_template("errors/403.html"), 403


@bp.app_errorhandler(404)
def error404(error):
    current_app.logger.error(f"{error} - url ingresada: {request.url}")
    return render_template("errors/400.html"), 404


@bp.app_errorhandler(500)
def error500(error):
    # si trabajas con db
    # db.session.rollback()
    # current_app.logger.error(error)
    return render_template("errors/500.html"), 500


@bp.app_errorhandler(502)
def error502(error):
    current_app.logger.error(error)
    return render_template("errors/502.html"), 502
