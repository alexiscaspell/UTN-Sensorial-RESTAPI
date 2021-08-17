from apps.models.indicador import Indicador
from apps.models.tablero import Tablero
from apps.repositories.entities.tablero_entity import TableroDocument
from apps.utils.mongo import mongo_connector
from typing import List
from apps.utils.mongo.mongo_connector import MongoQueryBuilder, get_by_filter


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
    query = MongoQueryBuilder(TableroDocument).add_id_filter(id).add_filter(
        {"indicadores.id": indicador_id}).add_return_field({"indicadores.$": 1}).build()

    tablero = mongo_connector.get_by_filter(query)

    if tablero is None or "indicadores" not in tablero:
        return None

    return Indicador.from_dict(tablero["indicadores"][0])
