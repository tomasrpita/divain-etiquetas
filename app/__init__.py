# coding: utf-8


import os
from flask import Flask
from config import config

# from app.LIB import reload_database

from app.logger import configure_logging
# from app.API import initialize_api



def create_app(config_name=(os.getenv("FLASK_CONFIG") or "default")):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configuración del gestor de logs
    configure_logging(app)
    app.logger.info("Inicio de Aplicación")

    # Inicialización del API
    # initialize_api()

    # Registra los Blueprints bajo el contexto de la app
    with app.app_context():

        # Registro de Blueprints de la App
        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.web import bp as web_bp
        app.register_blueprint(web_bp)

        # if config_name != "testing":
        #     from app.API import bp as api_bp
        #     app.register_blueprint(api_bp)

        # Recarga de la base de datos
        # reload_database.run()

        # Flask Shell
        @app.shell_context_processor
        def make_shell_context():
            pass

        @app.cli.command("sample_cli_script")
        def sample_cli_script():
            pass

    return app
