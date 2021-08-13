from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.usuario_service as user_service

URI = "/usuarios"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('', methods=['GET'])
def get_all_usuarios():
    result = [u.to_dict() for u in user_service.get_all_usuarios()]
    return jsonify(result), HTTPStatus.OK
