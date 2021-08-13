from apps.models.indicador import IndicadorRequest
from apps.models.app_model import AppModel
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object,get_body,get

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.indicador_service as indicador_service

URI = "/indicadores"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)

@blue_print.route('/<id_indicador>/calcular', methods=['POST'])
def calcular_indicador(id_indicador:str):
    body = get_body(request)
    body["id"] = id_indicador
    request_indicador = IndicadorRequest.from_dict(body)

    result = [r.to_dict() for r in indicador_service.procesar_indicador(request_indicador)]

    return jsonify(result), HTTPStatus.OK
