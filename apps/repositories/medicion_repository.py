from datetime import datetime
from typing import Dict, List

from apps.models.indicador import Indicador
from apps.models.medicion import Medicion
from apps.models.usuario import Usuario
from apps.repositories.entities.medicion_entity import MedicionDocument
from apps.utils.mongo import mongo_connector
from apps.utils.mongo.mongo_connector import MongoQueryBuilder


def guardar_varias(mediciones: List[Medicion]):
    return [mongo_connector.insert(MedicionDocument.from_model(m)) for m in mediciones]


def get_mediciones(mac: str, count: int = None, sort: dict = None) -> List[Medicion]:
    query = MongoQueryBuilder(MedicionDocument).add_filter(
        {"id_sensor": mac})
    if count:
        query = query.page(0, count)

    if sort:
        query = query.sort_by(sort)

    query = query.add_exclude_field("_id").build()

    resultados = mongo_connector.get_by_filter(query)

    return [Medicion.from_dict(r) for r in resultados]


def get_mediciones_por_fechas(mac: str, fecha_desde: datetime, fecha_hasta: datetime,sort=None) -> List[Medicion]:
    query = MongoQueryBuilder(MedicionDocument)

    filter_id = {"MAC": mac}

    filter_fecha_desde = {
        "fecha": {
            "$gt": fecha_desde
        }
    }

    filter_fecha_hasta = {
        "fecha": {
            "$lt": fecha_hasta
        }
    }

    query.filters(
        {"$and": [filter_id, filter_fecha_desde, filter_fecha_hasta]})

    if sort:
        query = query.sort_by(sort)

    resultados = mongo_connector.get_by_filter(query.build())

    return [Medicion.from_dict(r) for r in resultados]
