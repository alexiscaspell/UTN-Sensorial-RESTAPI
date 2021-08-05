from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.user_service as user_service

URI = "/usuarios"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('/hard', methods=['GET'])
def get_usuario_hard():
    return get_valid_rest_object(user_service.get_usuario_hard())