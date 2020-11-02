# coding: utf-8

import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler


def configure_logging(app):
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]
    # Añadimos el logger por defecto a la lista de loggers
    loggers = [
        app.logger,
    ]
    handlers = []
    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)
    # Creamos un manejador para los mensajes en fichero
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        f'logs/{app.config["APP_NAME"]}.log', maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(verbose_formatter())
    file_handler.setLevel(logging.INFO)
    handlers.append(file_handler)
    # Creamos un manejador para enviar los Archivos por eMail
    if app.config["MAIL_SERVER"]:
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr=app.config["EMAIL_FROM"],
            toaddrs=app.config["EMAIL_ADMINS"],
            subject=f'ATENCIÓN - Error en: {app.config["APP_NAME"]}',
            credentials=None,
        )
        mail_handler.setFormatter(verbose_formatter())
        mail_handler.setLevel(logging.ERROR)
        handlers.append(mail_handler)

    # Asociamos cada uno de los handlers a cada uno de los loggers
    for logger in loggers:
        for handler in handlers:
            logger.addHandler(handler)
        logger.propagate = False
        logger.setLevel(logging.DEBUG)


def verbose_formatter():
    return logging.Formatter(
        """[%(asctime)s.%(msecs)d] %(levelname)s
         \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s""",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
