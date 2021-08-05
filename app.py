import json
import os

from flask import Flask

import apps.configs.configuration as conf
from apps.configs.error_handlers import error_handler_bp
from apps.configs.vars import Vars
from apps.utils.blueprint_util import registrar_blue_prints

app = Flask(__name__)
app.register_blueprint(error_handler_bp)
registrar_blue_prints(app, 'apps/routes')

if __name__ == '__main__':

    possible_ports = [int(conf.get(Vars.API_PORT)), 80, 5000]

    for port in possible_ports:
        try:
            app.run(debug=conf.get(Vars.DEBUG_MODE),
                    host=conf.get(Vars.API_HOST), port=port)
            break
        except:
            continue
