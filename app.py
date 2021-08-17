import json
import os

from flask import Flask

import apps.configs.configuration as conf
from apps.configs.error_handlers import error_handler_bp
from apps.configs.vars import Vars
from apps.utils.blueprint_util import registrar_blue_prints
from mongoengine import connect
from apps.utils.logger_util import get_logger
from flask_cors import CORS
from apps.configs.vars import Vars
import apps.configs.configuration as conf

app = Flask(__name__)
app.register_blueprint(error_handler_bp)
CORS(app)
registrar_blue_prints(app, 'apps/routes')

logger = get_logger(__name__)

connect(host=conf.get(Vars.MONGODB_URL))

if __name__ == '__main__':

    possible_ports = [int(conf.get(Vars.API_PORT)), 80, 5000]

    for port in possible_ports:
        try:
            app.run(debug=conf.get(Vars.DEBUG_MODE),
                    host=conf.get(Vars.API_HOST), port=port)
            break
        except:
            continue
