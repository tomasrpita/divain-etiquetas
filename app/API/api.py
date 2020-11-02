# coding: utf-8

from flask_restful import Resource
from flask import jsonify

class ApiInicio(Resource):
    "WS de bienvenida (ejemplo)"

    def get(self):
        return jsonify({"Saludo": "Api funcionado"})


class ApiReference(Resource):
    def get(self, eanBotella):


        return {"Ean Botella": eanBotella}