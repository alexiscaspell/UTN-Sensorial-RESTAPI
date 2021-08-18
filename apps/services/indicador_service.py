from datetime import datetime, timedelta

from flask import json
from pandas.core.frame import DataFrame
from apps.models.sensor import Sensor
from apps.models.medicion import Medicion
from apps.models.indicador import Indicador, IndicadorRequest, IndicadorResult, TipoIndicador, UnidadTiempo, UnidadValor, IndicadorHistoricoRequest
from typing import Dict, List
from apps.repositories import tablero_repository
from apps.repositories import medicion_repository as mr
import pandas as pd

def _get_mediciones(sensor: str, count=None, desde=None, hasta=None) -> List[Medicion]:
    if count is not None:
        return mr.get_mediciones(sensor, count=count, sort={"fecha": "desc"})
    else:
        return mr.get_mediciones_por_fechas(sensor, fecha_desde=desde, fecha_hasta=hasta, sort={"fecha": "asc"})

def _group_df_por_tiempo(df:pd.DataFrame,unidad:UnidadTiempo):

    if unidad==UnidadTiempo.hora:
        funcion = lambda e: (e.year,e.month,e.day,e.hour)
    elif unidad==UnidadTiempo.dia:
        funcion = lambda e: (e.year,e.month,e.day)
    elif unidad==UnidadTiempo.semana:
        funcion = lambda e: e.isocalendar()[1]
    elif unidad==UnidadTiempo.mes:
        funcion = lambda e: (e.year,e.month)
    elif unidad==UnidadTiempo.anio:
        funcion = lambda e: e.year

    df["f_order"] = df["fecha"].apply(funcion )

    return df.groupby(by="f_order")


def _procesar_resultados(resultados: List[IndicadorResult], tipo_indicador: TipoIndicador, unidad_tiempo: UnidadTiempo) -> List[IndicadorResult]:
    for r in resultados:
        b = pd.DataFrame([e.to_dict() for e in r.valores])
        b["fecha"]=pd.to_datetime(b['fecha'])

        b["f_order"] = b["fecha"].apply(lambda e:e.isocalendar()[1])
        b = _group_df_por_tiempo(b,unidad_tiempo)
        b = b.mean(numeric_only=False)
        muestras_json = b.to_json(orient = 'records',date_format="iso")

        base = r.valores[0].to_dict()

        r.valores = [Medicion.from_dict({**base,**e}).valor for e in json.loads(muestras_json)]

    return resultados


def procesar_indicador_historico(request: IndicadorHistoricoRequest) -> List[IndicadorResult]:
    indicador: Indicador = tablero_repository.get_indicador(
        request.id_tablero, request.id)

    resultados = []

    unidad = UnidadValor.porcentaje if len(
        indicador.id_sensores) > 1 else UnidadValor.absoluto

    for s in indicador.id_sensores:
        mediciones = _get_mediciones(
            s, desde=request.desde, hasta=request.hasta)
        resultados.append(IndicadorResult(
            s, mediciones, unidad))

    return _procesar_resultados(resultados, indicador.tipo, unidad_tiempo=request.unidad)


def procesar_indicador_produccion(indicador: Indicador, request: IndicadorRequest) -> List[IndicadorResult]:
    request_historico = IndicadorHistoricoRequest({
        "id": request.id,
        "id_tablero": request.id_tablero,
        "unidad": UnidadTiempo.hora,
        "desde": datetime.now()-timedelta(hours=request.muestras),
        "hasta": datetime.now(),
    })
    return procesar_indicador_historico(request_historico)


def procesar_indicador(request_indicador: IndicadorRequest) -> List[IndicadorResult]:
    indicador: Indicador = tablero_repository.get_indicador(
        request_indicador.id_tablero, request_indicador.id)

    if indicador.tipo == TipoIndicador.produccion:
        return procesar_indicador_produccion(indicador, request_indicador)

    resultados = []

    unidad = UnidadValor.porcentaje if len(
        indicador.id_sensores) > 1 else UnidadValor.absoluto

    for id_sensor, mediciones in map(lambda s: (s, _get_mediciones(s, count=request_indicador.muestras)), indicador.id_sensores):
        resultados.append(IndicadorResult(
            id_sensor, [m.valor for m in mediciones], unidad))

    return resultados
