from typing import Dict, List

from apps.models.exception import UsuarioNotFoundException
from apps.models.sensor import Sensor
from apps.repositories.entities.sensor_entity import SensorDocument
from apps.utils.mongo import mongo_connector
from apps.utils.mongo.mongo_connector import MongoQueryBuilder


def _get_sensores():
    try:

        query = MongoQueryBuilder(SensorDocument).add_exclude_field("_id").build()
        resultados = mongo_connector.get_by_filter(query)

        if not resultados:
            return []

        return [Sensor.from_dict(r) for r in resultados]
    except Exception as _:
        pass

    return []

def get_all() -> List[Sensor]:
    return _get_sensores()

def save(sensor:Sensor):
    mongo_connector.insert(SensorDocument.from_model(sensor))