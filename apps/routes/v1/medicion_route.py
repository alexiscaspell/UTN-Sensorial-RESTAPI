from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_body

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

@blue_print.route('/mock', methods=['POST'])
def mock_mediciones():
    body = get_body(request)

    if "desde" in body:
        desde = datetime.fromisoformat(body["desde"])
    else:
        desde=datetime.now()
        desde.month-=1

    if "hasta" in body:
        hasta = datetime.fromisoformat(body["hasta"])
    else:
        hasta=datetime.now()

    medicion_service.hardcodear(body.get("cantidad",10), desde=desde, hasta=hasta, variacion=body.get("variacion",0.15),tipos=body.get("tipos",None))

    return '', 200
