from flask import Blueprint, jsonify, request,send_file
from io import BytesIO
import apps.configs.configuration as var
from apps.utils.logger_util import get_logger
from apps.models.exception import AppException
import os
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

@blue_print.route('/postman')
def download_postman_collection():
    postman_files = sorted([
        f for f in os.listdir(os.getcwd())
        if str(f).endswith('.postman_collection.json')
    ], reverse=True)

    collection_dir = next(iter(postman_files), None)

    return send_file(BytesIO(open(collection_dir, 'rb').read()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=os.path.basename(collection_dir))