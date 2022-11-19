# coding: utf-8

from flask_restful import Resource
from app.LIB.reference_controller import get_reference_data




class ApiReference(Resource):
    def get(self, eanBotella):

        resp = {
            'status': 'ok',
                    }
        resp.update(get_reference_data(eanBotella))

        return resp
