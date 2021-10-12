from apps.models.objetivo import Objetivo
from typing import List

from apps.models.indicador import Indicador
from apps.models.reporte import Reporte
from apps.models.tablero import Tablero
from apps.repositories.entities.tablero_entity import TableroDocument
from apps.utils.mongo import mongo_connector
from apps.utils.mongo.mongo_connector import MongoQueryBuilder
from bson import ObjectId
from apps.models.exception import IndicadorNotFoundException, ObjetivoNotFoundException, ReporteInvalidoException, TableroNotFoundException, ReporteYaExistenteException


def _get_tableros():

    query = MongoQueryBuilder(
        TableroDocument).add_exclude_field("_id").add_exclude_field("__v").build()

    resultados = mongo_connector.get_by_filter(query)

    if not resultados:
        return []

    return [Tablero.from_dict(r) for r in resultados]


def get_all() -> List[Tablero]:
    return _get_tableros()


def get_tablero_by_reporte(id_reporte: str) -> Tablero:
    query = MongoQueryBuilder(
        TableroDocument).add_exclude_field("_id").add_exclude_field("__v")

    query.add_id_filter({"reportes": id_reporte})

    result = mongo_connector.get_by_filter(query.build())

    if result is None or len(result) == 0:
        raise ReporteInvalidoException(id_reporte)

    return Tablero.from_dict(result[0])


def _get_by_id(id_tablero: str) -> dict:
    result = mongo_connector.get_by_id(TableroDocument, id_tablero)

    if result is None:
        raise TableroNotFoundException(id_tablero)

    return result


def get_by_id(id: str) -> Tablero:
    r = _get_by_id(id)
    return Tablero.from_dict(r)


def add_reporte(id_tablero: str, reporte: Reporte) -> Reporte:
    result = _get_by_id(id_tablero)

    for r in result["reportes"]:
        if r["nombre"] == reporte.nombre:
            raise ReporteYaExistenteException(reporte.nombre)

    reporte.id = str(ObjectId())
    result["reportes"].append(reporte.to_dict())

    TableroDocument.easy_update_one(id_tablero, result)

    return reporte


def get_all_reportes() -> List[Reporte]:
    reportes = []

    for t in get_all():
        reportes += t.reportes

    return reportes


def get_indicador(id: str, indicador_id: str) -> Indicador:
    # query = MongoQueryBuilder(TableroDocument).add_id_filter(id).build()
    # query = MongoQueryBuilder(TableroDocument).add_id_filter(id).add_id_filter({"indicadores":indicador_id}).add_slice_field("indicadores", 0, 1).build()

    result = mongo_connector.get_by_id(TableroDocument, id)

    if result is None or len(result.get("indicadores")) == 0:
        raise IndicadorNotFoundException(indicador_id)

    indicador_result = None

    for i in result["indicadores"]:
        if i["id"] == indicador_id:
            indicador_result = i
            break

    if indicador_result is None:
        raise IndicadorNotFoundException(indicador_id)

    return Indicador.from_dict(indicador_result)


def get_objetivo(id: str, objetivo_id: str) -> Objetivo:
    query = MongoQueryBuilder(TableroDocument).add_id_filter(id).build()
    # query = MongoQueryBuilder(TableroDocument).add_id_filter(id).add_id_filter({"indicadores":indicador_id}).add_slice_field("indicadores", 0, 1).build()

    result = mongo_connector.get_by_filter(query)

    if result is None or len(result) == 0 or len(result[0].get("objetivos")) == 0:
        raise ObjetivoNotFoundException(objetivo_id)

    objetivo_result = None

    for i in result[0]["objetivos"]:
        if i["id"] == objetivo_id:
            objetivo_result = i
            break

    if objetivo_result is None:
        return None

    return Objetivo.from_dict(objetivo_result)


def delete_reporte(id_tablero: str, id_reporte: str):
    result = _get_by_id(id_tablero)

    reportes = list(
        filter(lambda r: r['id'] != id_reporte, result["reportes"]))

    result["reportes"] = reportes

    TableroDocument.easy_update_one(id_tablero, result)
