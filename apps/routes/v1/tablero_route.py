from apps.models.indicador import IndicadorRequest, IndicadorHistoricoRequest
from apps.models.app_model import AppModel
from http import HTTPStatus
from flask_cors import cross_origin

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import  get_body

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.indicador_service as indicador_service
import apps.services.tablero_service as tablero_service
import apps.services.objetivo_service as objetivo_service
from apps.models.indicador import IndicadorResultList
from apps.models.reporte import Reporte
from apps.models.exception import InvalidIdException

URI = "/tableros"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


def validate_id(entidad:str,id):
    str_id=str(id).strip()

    id_vacio = id is None or str_id==""
    id_invalido=str_id=="null" or str_id=="undefined"

    if id_vacio or id_invalido:
        raise InvalidIdException(entidad,str_id)



@cross_origin()
@blue_print.route('/<id_tablero>/objetivos/<id_objetivo>/calculado', methods=['GET'])
def calcular_objetivo(id_tablero: str, id_objetivo: str):

    validate_id("Tablero",id_tablero)
    validate_id("Objetivo",id_objetivo)

    result = objetivo_service.procesar_objetivo(id_tablero, id_objetivo)

    return jsonify(result.to_dict()), HTTPStatus.OK

@cross_origin()
@blue_print.route('/<id_tablero>/indicadores/<id_indicador>/calculado', methods=['POST'])
def calcular_indicador(id_tablero: str, id_indicador: str):
    body = get_body(request)
    body["id"] = id_indicador
    body["id_tablero"] = id_tablero

    validate_id("Tablero",id_tablero)
    validate_id("Indicador",id_indicador)

    request_indicador = IndicadorRequest.from_dict(body)

    result = IndicadorResultList(indicador_service.procesar_indicador(request_indicador)).to_json()

    return jsonify(result), HTTPStatus.OK

@cross_origin()
@blue_print.route('/<id_tablero>/indicadores/<id_indicador>/historico', methods=['POST'])
def calcular_indicador_historico(id_tablero: str, id_indicador: str):
    body = get_body(request)
    body["id"] = id_indicador
    body["id_tablero"] = id_tablero

    validate_id("Tablero",id_tablero)
    validate_id("Indicador",id_indicador)

    request_indicador = IndicadorHistoricoRequest.from_dict(body)

    result = IndicadorResultList(indicador_service.procesar_indicador_historico(
        request_indicador)).to_json()

    return jsonify(result), HTTPStatus.OK

@cross_origin()
@blue_print.route('/<id_tablero>/reportes/<id_reporte>', methods=['DELETE'])
def eliminar_reporte(id_tablero: str, id_reporte: str):

    validate_id("Tablero",id_tablero)
    validate_id("Reporte",id_reporte)

    tablero_service.borrar_reporte(id_tablero,id_reporte)
    return jsonify({}), HTTPStatus.OK

@cross_origin()
@blue_print.route('/<id_tablero>/reportes', methods=['POST'])
def guardar_reporte(id_tablero: str):
    body = get_body(request)
    reporte = Reporte.from_dict(body)

    validate_id("Tablero",id_tablero)

    return jsonify(tablero_service.guardar_reporte(id_tablero,reporte).to_dict()), HTTPStatus.CREATED


@blue_print.route('', methods=['GET'])
def get_all():
    result = [t.to_dict() for t in tablero_service.get_all()]

    return jsonify(result), HTTPStatus.OK