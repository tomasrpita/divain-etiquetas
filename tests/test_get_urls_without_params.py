# coding: utf-8
"Prueba las rutas que admiten get y que no reciban parametros en la app"

import unittest
from flask import current_app, url_for
from app import create_app
from app.database import db


def has_no_empty_params(rule):
    """
    Comprueba si una url (endpoint) tiene o no parmetros.
    Parmetos:
    - rule: url (endpoint)
    Retorna:
    - True cuando la url (endpoint) no tiene parmetros, False cuando s los tiene
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def site_map_urls_no_need_params(app):
    """
    Obtiene la lista de urls's (end points) de la aplicacion que no necesiten 
    parametros para acceder
    
    Parametos:
    - app: aplicacion
    Retorna:
    - Lista de tuplas (url, blueprint+funcion) de la aplicacion que no necesiten
    parametros para acceder
    """
    links = []
    # Recorre la lista de toda slas url's (end points) de la aplicacion
    for rule in app.url_map.iter_rules():
        # Filtrar las reglas que no podemos navegar en un navegador y las reglas 
        # que requieren parámetros.
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    # Retorna el diccionario de url's que no necesiten parametros para acceder
    return dict(links)


class TestGetUrlsWithoutParams(unittest.TestCase):
    def setUp(self):
        """Define las variables del test e inicializa la app"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        db.create_all()

    def tearDown(self):
        """Metodo que se ejecutal al final ddel test para deconstruir el 
        aparato de prueba después de probarlo."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_urls(self):
        "Prueba las rutas que admiten get y que no reciban parametros en la app"

        links = site_map_urls_no_need_params(self.app)
        for link in links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)
