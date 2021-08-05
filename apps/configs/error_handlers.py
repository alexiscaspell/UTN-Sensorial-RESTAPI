from apps.utils.logger_util import get_logger
from apps.models.exception import AppException
from flask import Blueprint, jsonify, request
from http import HTTPStatus

error_handler_bp = Blueprint('errors_handlers', __name__)

logger = get_logger()


@error_handler_bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
    return '', HTTPStatus.NOT_FOUND


@error_handler_bp.app_errorhandler(Exception)
def handle_exception(e):
    get_logger().exception(str(e))
    return '', HTTPStatus.INTERNAL_SERVER_ERROR


@error_handler_bp.app_errorhandler(AppException)
def handle_business_exception(ae: AppException):
    return ae.respuesta_json()
