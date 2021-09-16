from typing import Dict, List

from apps.models.sensor import Sensor
from apps.repositories.entities.sensor_entity import SensorDocument
from apps.utils.mongo import mongo_connector
from apps.utils.mongo.mongo_connector import MongoQueryBuilder


def _get_sensores():
    try:
        query = MongoQueryBuilder(
            SensorDocument).add_exclude_field("_id").build()
        resultados = mongo_connector.get_by_filter(query)

        if not resultados:
            return []

        return [Sensor.from_dict(r) for r in resultados]
    except Exception as _:
        pass

    return []


def get_all() -> List[Sensor]:
    return _get_sensores()


def save_all(sensores: List[Sensor]):
    macs = list(set(map(lambda s:s.MAC,sensores)))

    query = MongoQueryBuilder(SensorDocument).add_exclude_field("_id")
    query.add_exclude_field("id")
    query.add_filter({"MAC":{"$in":macs}})

    resultados = mongo_connector.get_by_filter(query.build())

    macs_encontradas = list(map(lambda r:r["MAC"],resultados))

    for s in sensores:
        if s.MAC in macs_encontradas:
            continue

        save(s)
    # SensorDocument.easy_update_one_by_key("MAC",s.MAC,SensorDocument.from_model(s).to_dict(),args={"upsert":True})


def save(sensor: Sensor):
    mongo_connector.insert(SensorDocument.from_model(sensor))
