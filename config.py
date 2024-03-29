# coding: utf-8
import os


class Config(object):


    SECRET_KEY = os.environ.get("SECRET_KEY") or "tu-nunca-la-sabras"

    # Configuración para recibir notificaciones por correo
    MAIL_SERVER = None
    APP_NAME = "Divain Etiquetas"

    LABELS_INFO_URL = os.environ.get("LABELS_INFO_URL") or "https://divain.pro/api/references/labels-info/"

    BASE_URL = os.environ.get("BASE_URL") or "https://divain.pro/"
    PRODUCTION_ORDER_URL = os.environ.get("PRODUCTION_ORDER_URL") or "api/production-order-label/"


class TestingConfig(Config):
    """
    Configuración para ejecución en modo TEST
    """

    TESTING = True
    DEBUG = False
    SERVER_NAME = "localhost"


class DevelopmentConfig(Config):
    """
    Configuración para ejecución en modo Development
    """


class ProductionConfig(Config):
    """
    Configuración para ejecución en modo Development
    """


config = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
