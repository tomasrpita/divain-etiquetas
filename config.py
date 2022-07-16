# coding: utf-8
import os


class Config(object):


    SECRET_KEY = os.environ.get("SECRET_KEY") or "tu-nunca-la-sabras"

    # Configuración para recibir notificaciones por correo
    MAIL_SERVER = None
    APP_NAME = "Divain Etiquetas"


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
