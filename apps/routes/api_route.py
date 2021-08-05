from flask import Blueprint, jsonify, request

import apps.configs.configuration as var
from apps.utils.logger_util import get_logger
from apps.models.exception import AppException

blue_print = Blueprint('api', __name__, url_prefix='')

logger = get_logger()


@blue_print.route('/vars')
def variables():
    return jsonify(var.variables_cargadas())


@blue_print.route('/errors')
def error():
    raise AppException('PRUEBA', 'No Wanda Nara!')


@blue_print.route('/alive')
def vivo():
    logger.info("VIVO")
    return jsonify({"estado": "vivo"})