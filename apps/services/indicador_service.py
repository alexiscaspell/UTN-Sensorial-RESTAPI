from apps.models.sensor import Sensor
from apps.models.medicion import Medicion
from apps.models.indicador import Indicador, IndicadorRequest, IndicadorResult, TipoIndicador, UnidadValor
from typing import Dict, List
from apps.repositories import tablero_repository
from apps.repositories import medicion_repository as mr


def _get_mediciones(sensor: Sensor, request_indicador: IndicadorRequest)->List[Medicion]:
    return mr.get_mediciones(sensor.id, count=request_indicador.muestras,sort=("fecha","desc"))

def procesar_indicador_produccion(indicador:Indicador,request:IndicadorRequest)->List[IndicadorResult]:
    raise NotImplementedError("No se sabe procesar aun un indicador de produccion")


def procesar_indicador(request_indicador: IndicadorRequest) -> List[IndicadorResult]:
    indicador: Indicador = tablero_repository.get_indicador(request_indicador.id_tablero,request_indicador.id)

    if indicador.tipo==TipoIndicador.produccion:
        return procesar_indicador_produccion(indicador,request_indicador)
    
    resultados = []

    unidad = UnidadValor.porcentaje if len(
        indicador.sensores) > 1 else UnidadValor.absoluto

    for id_sensor, mediciones in map(lambda s: (s.id, _get_mediciones(s, request_indicador)), indicador.sensores):
        resultados.append(IndicadorResult(
            id_sensor,[m.valor for m in mediciones], unidad))

    return resultados
