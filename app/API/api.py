# coding: utf-8

from flask_restful import Resource
from flask import jsonify

from app.LIB.reference_controller import get_reference_data

class ApiInicio(Resource):
    "WS de bienvenida (ejemplo)"

    def get(self):
        return jsonify({"Saludo": "Api funcionado"})


class ApiReference(Resource):
    def get(self, eanBotella):

        resp = {
            'status': 'ok',
                    }
        resp.update(get_reference_data(eanBotella))

        return resp