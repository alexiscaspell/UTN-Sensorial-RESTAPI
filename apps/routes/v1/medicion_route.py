from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object,get_body

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.medicion_service as medicion_service
from apps.models.medicion import MedicionRaspberry

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
