from apps.models.indicador import IndicadorRequest, IndicadorHistoricoRequest
from apps.models.app_model import AppModel
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object, get_body

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.indicador_service as indicador_service
import apps.services.tablero_service as tablero_service

URI = "/tableros"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('/<id_tablero>/indicadores/<id_indicador>/calculado', methods=['POST'])
def calcular_indicador(id_tablero: str, id_indicador: str):
    body = get_body(request)
    body["id"] = id_indicador
    body["id_tablero"] = id_tablero

    request_indicador = IndicadorRequest.from_dict(body)

    result = [r.to_dict()
              for r in indicador_service.procesar_indicador(request_indicador)]

    return jsonify(result), HTTPStatus.OK


@blue_print.route('/<id_tablero>/indicadores/<id_indicador>/historico', methods=['POST'])
def calcular_indicador_historico(id_tablero: str, id_indicador: str):
    body = get_body(request)
    body["id"] = id_indicador
    body["id_tablero"] = id_tablero

    request_indicador = IndicadorHistoricoRequest.from_dict(body)

    result = [r.to_dict() for r in indicador_service.procesar_indicador_historico(
        request_indicador)]

    return jsonify(result), HTTPStatus.OK


@blue_print.route('', methods=['GET'])
def get_all():
    result = [t.to_dict() for t in tablero_service.get_all()]

    return jsonify(result), HTTPStatus.OK
