from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object,wrap_rest_response

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.tasks_service as tasks_service
from apps.utils.rest_util import get_body
from apps.models.tarea_programada import TareaProgramada

URI = "/tareas"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('', methods=['GET'])
def get_tareas():
    result = [e.to_dict() for e in tasks_service.get_tareas()]

    return jsonify(result),HTTPStatus.OK

@blue_print.route('', methods=['POST'])
def post_tarea_programada():
    tarea = TareaProgramada.from_dict(get_body(request))

    result = tasks_service.agregar_tarea(tarea)

    return jsonify(result),HTTPStatus.CREATED

@blue_print.route('/<id_tarea>', methods=['PATCH'])
def patch_tarea_programada(id_tarea):
    atributos_nuevos = get_body(request)

    result = tasks_service.actualizar_atributos_tarea(id_tarea,atributos_nuevos)

    return jsonify(result),HTTPStatus.OK

@blue_print.route('/<id_tarea>/run', methods=['GET'])
def correr_tarea_programada(id_tarea):

    tasks_service.ejecutar_tarea(id_tarea,force_run=True)

    return jsonify({}),HTTPStatus.OK

@blue_print.route('/<id_tarea>', methods=['DELETE'])
def delete_tarea_programada(id_tarea):
    tasks_service.eliminar_tarea(id_tarea)

    return jsonify({}),HTTPStatus.OK

@blue_print.route('', methods=['DELETE'])
def delete_all():
    body = get_body(request)

    conservar = str(body.get("conservar","false"))=="true"

    ids_tareas = [e.id for e in tasks_service.get_tareas()]

    ids = body.get("ids",ids_tareas)

    for id_tarea in ids_tareas:
        if (id_tarea in ids and not conservar) or (id_tarea not in ids and conservar):
            tasks_service.eliminar_tarea(id_tarea)

    return jsonify({}),HTTPStatus.OK