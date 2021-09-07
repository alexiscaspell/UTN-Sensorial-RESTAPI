from typing import List

from apps.models.indicador import Indicador
from apps.models.tablero import Tablero
from apps.repositories.entities.tablero_entity import TableroDocument
from apps.utils.mongo import mongo_connector
from apps.utils.mongo.mongo_connector import MongoQueryBuilder, get_by_filter
from bson import ObjectId
from apps.models.exception import IndicadorNotFoundException


def _get_tableros():
    # try:

    query = MongoQueryBuilder(
        TableroDocument).add_exclude_field("_id").add_exclude_field("__v").build()
    resultados = mongo_connector.get_by_filter(query)

    if not resultados:
        return []

    return [Tablero.from_dict(r) for r in resultados]
    # except Exception as _:
    #     pass

    return []


def get_all() -> List[Tablero]:
    return _get_tableros()


def get_indicador(id: str, indicador_id: str) -> Indicador:
    query = MongoQueryBuilder(TableroDocument).add_id_filter(id).build()
    # query = MongoQueryBuilder(TableroDocument).add_id_filter(id).add_id_filter({"indicadores":indicador_id}).add_slice_field("indicadores", 0, 1).build()

    result = mongo_connector.get_by_filter(query)

    if result is None or len(result) == 0 or "indicadores" not in result[0]:
        raise IndicadorNotFoundException(indicador_id)

    indicador_result=None

    for i in result[0]["indicadores"]:
        if i["id"]==indicador_id:
            indicador_result = i
            break

    if indicador_result is None:
        return None

    return Indicador.from_dict(indicador_result)
