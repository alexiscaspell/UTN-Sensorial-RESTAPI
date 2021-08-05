from http import HTTPStatus

from flask import Blueprint, jsonify, request
from apps.utils.rest_util import get_valid_rest_object

import apps.configs.configuration as conf
from apps.configs.vars import Vars
import apps.services.ejemplo_service as ejemplo_service

URI = "/ejemplo"
VERSION = "/v1"

blue_print = Blueprint(URI,
                       __name__,
                       url_prefix=conf.get(Vars.API_BASE_PATH)+VERSION+URI)


@blue_print.route('', methods=['GET'])
def get_ejemplo():

    return get_valid_rest_object(ejemplo_service.get_ejemplo())