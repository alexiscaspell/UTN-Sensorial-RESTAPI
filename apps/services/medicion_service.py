from typing import List
import apps.configs.configuration as conf
from apps.configs.vars import Vars
from apps.models.sensor import Sensor

from apps.models.medicion import MedicionRaspberry
from apps.repositories import medicion_repository as medicion_repository
from apps.repositories import sensor_repository as sensor_repository


def guardar_mediciones(mediciones_raspberry: List[MedicionRaspberry]):
    mediciones = [m.to_medicion() for m in mediciones_raspberry]

    if conf.get(Vars.AUTOCREAR_SENSORES):
        sensores = list(set(map(lambda m: Sensor.from_dict({"tipo":m.tipo_sensor,"MAC":m.MAC,"nombre":m.MAC}),mediciones)))
        sensor_repository.save_all(sensores)

    medicion_repository.guardar_varias(mediciones)
