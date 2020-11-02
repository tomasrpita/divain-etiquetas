# coding: utf-8

from flask import Blueprint
from flask_restful import Api
from .api import (
    ApiInicio,
    ApiReference
)


bp = Blueprint("API", __name__, url_prefix="/api")


def initialize_api():
    """
    Inicia la Api
    """
    api = Api(bp)
    initialize_routes(api)


def initialize_routes(api):
    """
    Inicia las rutas de la Api
    """
    api.add_resource(ApiInicio, "/")
    api.add_resource(ApiReference, "/reference/<string:eanBotella>")
