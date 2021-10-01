from typing import List
import apps.configs.configuration as conf
from apps.configs.vars import Vars
from apps.models.sensor import Sensor

from apps.models.medicion import MedicionRaspberry
from apps.repositories import medicion_repository as medicion_repository
from apps.repositories import sensor_repository as sensor_repository
from datetime import datetime
from datetime import timedelta
import random


def guardar_mediciones(mediciones_raspberry: List[MedicionRaspberry]):
    mediciones = [m.to_medicion() for m in mediciones_raspberry]

    if conf.get(Vars.AUTOCREAR_SENSORES,tipo=bool):
        sensores = list(set(map(lambda m: Sensor.from_dict({"tipo":m.tipo_sensor,"MAC":m.MAC,"nombre":m.MAC}),mediciones)))
        sensor_repository.save_all(sensores)

    medicion_repository.guardar_varias(mediciones)

def hardcodear(count: int, date_init: datetime, date_final: datetime, time_delta: int):

    sensor_types = ['temperatura', 'humedad', 'calidad_del_aire', 'produccion']

    sensor_types = {
        'temperatura': {
            'macs': ['T1', 'T2', 'T3'],
            'unit': 'ºC'
        },
        'humedad': {
            'macs': ['H1', 'H2', 'H3'],
            'unit': '% HR'
        },
        'calidad_del_aire': {
            'macs': ['A1', 'A2', 'A3'],
            'unit': 'PPM CO2'
        },
        'produccion': {
            'macs': ['P1', 'P2', 'P3'],
            'unit': 'bool'
        }
    }

    mediciones=[]

    for sensor_type, conf in sensor_types.items():
        
        base_creation_date = random_date(date_init, date_final, time_delta)
        
        for mac in conf.get('macs'):
            for n in range(0, count):

                value = random_value(sensor_type)
                creation_date = base_creation_date + timedelta(milliseconds=random.randint(1, 418969))

                m = MedicionRaspberry.from_dict(
                    {"mac":mac,
                    "sensor_type":sensor_type,
                    "value":value,
                    "unit":conf.get('unit'),
                    "creation_date":creation_date}
                )

                mediciones.append(m)

    guardar_mediciones(mediciones)


def random_value(sensor_type: str) -> int:

    if sensor_type == 'temperatura':
        return random.randint(15, 35)

    if sensor_type == 'humedad':
        return random.randint(50, 95)

    if sensor_type == 'calidad_del_aire':
        return random.randint(50, 90)

    if sensor_type == 'produccion':
        return random.randint(0, 2)


def random_date(date_init: datetime = None, date_final: datetime = None, time_delta: int = None):

    if time_delta and date_init and date_final:

        while True:
            date_result = _random_date(time_delta)
            if date_init < date_result < date_final:
                return date_result

    if date_init and date_final:
        time_rnd = date_init.timestamp() + random.random() * (date_final.timestamp() -
                                                              date_init.timestamp())
        time_rnd += (random.randint(0, 60) + random.randint(0, 60) *
                     60 + random.randint(0, 60) * 3600)
        return datetime.fromtimestamp(time_rnd)

    return datetime.now() + (timedelta(minutes=20 * random.random()) * (-1)**int(random.randint(1, 2)))


def _random_date(time_delta: int):
    cte = 10
    time_rnd = random.randint(1, cte) * time_delta * 1000

    time_add = timedelta(milliseconds=time_rnd)
    return datetime.now() + time_add * (-1)**(random.randint(1, 2))
