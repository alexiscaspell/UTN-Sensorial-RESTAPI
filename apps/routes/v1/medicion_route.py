from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object,get_body

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.medicion_service as medicion_service
from apps.models.medicion import MedicionRaspberry
from datetime import datetime

URI = "/mediciones"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('', methods=['POST'])
def post_mediciones():
    body = get_body(request)

    mediciones = [MedicionRaspberry.from_dict(e) for e in body]

    return jsonify(medicion_service.guardar_mediciones(mediciones)), HTTPStatus.CREATED

@blue_print.route('/mock', methods=['GET'])
def mock_mediciones():

    count = int(request.args.get('count', 3))
    date_init = request.args.get('date_init')
    date_final = request.args.get('date_final')
    time_delta = request.args.get('time_delta')

    if date_init:
        date_init = datetime.fromisoformat(date_init)

    if date_final:
        date_final = datetime.fromisoformat(date_final)

    if time_delta == 'minutes':
        time_delta = 60

    if time_delta == 'hours':
        time_delta = 60 ** 2

    if time_delta == 'days':
        time_delta = 24 * 60 ** 2

    medicion_service.hardcodear(count, date_init, date_final, time_delta)

    return '', 200
