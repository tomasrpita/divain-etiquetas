# coding: utf-8

"Prueba Basicas"
import unittest
from flask import current_app
from app import create_app
from app.database import db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """Define las variables del test e inicializa la app"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Metodo que se ejecutal al final ddel test para deconstruir el
        aparato de prueba después de probarlo."""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        "Prueba que la aplicación ha sido creada"
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        "Prueba que estemos corriendo en modo testing"
        self.assertTrue(current_app.config["TESTING"])
