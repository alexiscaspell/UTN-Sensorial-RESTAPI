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

def _valor_medicion_random(sensor_type: str,anterior=None,variacion=0.15) -> int:
    if not anterior:
        if sensor_type == 'temperatura':
            anterior = random.randint(15, 35)

        if sensor_type == 'humedad':
            anterior = random.randint(50, 95)

        if sensor_type == 'calidad_del_aire':
            anterior = random.randint(50, 90)

        if sensor_type == 'produccion':
            anterior = random.randint(0, 2)

    return anterior * (1 + ((-1)**random.randint(0,2)) * random.uniform(0, variacion))

def hardcodear(cantidad: int, desde: datetime, hasta: datetime, variacion: float=0.15,tipos=None):

    tipos = ['temperatura', 'humedad', 'calidad_del_aire', 'produccion'] if tipos is None else tipos

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

    max_milisegundos = (hasta-desde).total_seconds()*1000
    step_milisegundos = int(max_milisegundos/cantidad)

    for sensor_type, conf in sensor_types.items():

        if sensor_type not in tipos:
            continue
        
        base_creation_date = desde
        
        for _ in range(0, cantidad):
            for i,mac in enumerate(conf.get('macs')):
                indice_anterior = len(mediciones)-i-len(conf.get('macs'))-1
                anterior = mediciones[indice_anterior].value if indice_anterior>=0 else None

                valor = _valor_medicion_random(sensor_type,anterior,variacion)

                fecha = base_creation_date + timedelta(milliseconds=random.randint(0,step_milisegundos))

                m = MedicionRaspberry.from_dict(
                    {"mac":mac,
                    "sensor_type":sensor_type,
                    "value":valor,
                    "unit":conf.get('unit'),
                    "creation_date":fecha}
                )

                mediciones.append(m)

            base_creation_date+=timedelta(milliseconds=step_milisegundos)

    guardar_mediciones(mediciones)