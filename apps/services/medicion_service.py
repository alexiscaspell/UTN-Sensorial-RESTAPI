from apps.utils.logger_util import get_logger
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
import threading

logger = get_logger(__name__)


def guardar_mediciones(mediciones_raspberry: List[MedicionRaspberry]):

    logger.info(f"GUARDANDO {len(mediciones_raspberry)} MEDICIONES ...")

    mediciones = [m.to_medicion() for m in mediciones_raspberry]

    if conf.get(Vars.AUTOCREAR_SENSORES, tipo=bool):
        sensores = list(set(map(lambda m: Sensor.from_dict(
            {"tipo": m.tipo_sensor, "MAC": m.MAC, "nombre": m.MAC}), mediciones)))
        sensor_repository.save_all(sensores)

    medicion_repository.guardar_varias(mediciones)


def _valor_medicion_random(sensor_type: str, anterior=None, variacion=0.15, limites=[0, 0],limites_activo=False) -> int:
    minimo = limites[0]
    maximo = limites[1]

    if not anterior:
        anterior = random.randint(minimo, maximo)

    anterior = anterior * (1 + ((-1)**random.randint(0, 2))
                           * random.uniform(0, variacion))

    if limites_activo:
        anterior = min(anterior,maximo)
        anterior = max(anterior,minimo)

    return anterior


def hardcodear(desde: datetime, hasta: datetime, variacion: float = 0.15, tipos=None, cantidad: int = None, periodo=None, limites=None,sensors={}):
    tipos = ['temperatura', 'humedad', 'calidad_del_aire',
             'produccion'] if tipos is None else tipos

    sensor_types_base = {
        'temperatura': {
            'macs': sensors["temperatura"]["macs"] if "temperatura" in sensors else ['T1', 'T2', 'T3'],
            'unit': 'ºC'
        },
        'humedad': {
            'macs': sensors["temperatura"]["macs"] if "humedad" in sensors else ['H1', 'H2', 'H3'],
            'unit': '% HR'
        },
        'calidad_del_aire': {
            'macs': sensors["temperatura"]["macs"] if "calidad_del_aire" in sensors else ['A1', 'A2', 'A3'],
            'unit': 'PPM CO2'
        },
        'produccion': {
            'macs': sensors["temperatura"]["macs"] if "produccion" in sensors else ['P1', 'P2', 'P3'],
            'unit': 'bool'
        }
    }

    sensor_types = sensor_types_base

    for type in sensor_types_base:
        if type not in sensors:
            sensor_types.pop(type,None)

    limites_activo= limites is not None

    if not limites:
        limites = {
            "temperatura": [15, 35],
            "humedad": [50, 95],
            "calidad_del_aire": [50, 90],
            "produccion": [0, 2]
        }

    mediciones = {}

    for _, conf in sensor_types.items():
        for mac in conf.get('macs'):
            mediciones.update({mac: []})

    max_milisegundos = (hasta-desde).total_seconds()*1000

    if cantidad is None and periodo is not None:
        cantidad = int(max_milisegundos/(max(periodo, 1)*1000))

    step_milisegundos = int(max_milisegundos/cantidad)

    logger.info(f"HARDCODEANDO {cantidad}*{sum([len(sensor_types[t]['macs']) for t in tipos])} MEDICIONES ...")
    logger.info(f"TIPOS A HARDCODEAR: {tipos}")

    for sensor_type, conf in sensor_types.items():

        if sensor_type not in tipos:
            continue

        base_creation_date = desde

        for _ in range(0, cantidad):
            for i, mac in enumerate(conf.get('macs')):
                anterior = mediciones[mac][-1].value if len(
                    mediciones[mac]) > 0 else None

                valor = _valor_medicion_random(
                    sensor_type, anterior, variacion,limites[sensor_type],limites_activo)

                fecha = base_creation_date + \
                    timedelta(milliseconds=random.randint(
                        0, step_milisegundos))

                m = MedicionRaspberry.from_dict(
                    {"mac": mac,
                     "sensor_type": sensor_type,
                     "value": valor,
                     "unit": conf.get('unit'),
                     "creation_date": fecha}
                )

                mediciones[mac].append(m)

            base_creation_date += timedelta(milliseconds=step_milisegundos)

    reverse = datetime.now() > desde

    mediciones = sum(mediciones.values(), [])
    mediciones = list(reversed(mediciones) if reverse else mediciones)

    logger.info(f"ENVIANDO VALORES HARDCODEADOS A DB ...")

    a = threading.Thread(target=_guardar_mediciones_async,
                         args=[mediciones], daemon=True)
    a.start()


def _guardar_mediciones_async(mediciones):
    logger.info(f"INSERTANDO {len(mediciones)} MEDICIONES ASINCRONAMENTE")
    guardar_mediciones(mediciones)
    logger.info(f"INSERCION ASINCRONA TERMINADA.")
