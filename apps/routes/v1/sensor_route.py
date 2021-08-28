from http import HTTPStatus
import re

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_body, get_valid_rest_object

import apps.configs.configuration as conf
from apps.configs.vars import Vars
from apps.models.sensor import Sensor
import apps.services.sensor_service as sensores_service

URI = "/sensores"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('', methods=['GET'])
def get_all_sensores():
    result = [s.to_dict() for s in sensores_service.get_all_sensores()]
    return jsonify(result), HTTPStatus.OK

@blue_print.route('', methods=['POST'])
def crear_sensor():
    sensor = Sensor.from_dict(get_body(request))

    return jsonify(sensores_service.guardar(sensor)), HTTPStatus.CREATED
