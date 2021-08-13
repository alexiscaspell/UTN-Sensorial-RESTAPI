from apps.models.sensor import Sensor
from apps.models.medicion import Medicion
from apps.models.indicador import Indicador, IndicadorRequest, IndicadorResult, Unidad
from typing import Dict, List
from apps.repositories import indicador_repository
from apps.repositories import sensor_repository as sr


def _get_mediciones(sensor: Sensor, request_indicador: IndicadorRequest)->List[Medicion]:
    if(request_indicador.muestras):
        muestras_totales = sr.contar_mediciones(sensor.id)

        step = round(request_indicador.muestras/muestras_totales)

        return sr.get_mediciones(sensor.id, step=step, count=request_indicador.muestras)
    else:
        return sr.get_mediciones_por_fechas(sensor.id, request_indicador.desde, request_indicador.hasta)


def procesar_indicador(request_indicador: IndicadorRequest) -> List[IndicadorResult]:
    indicador: Indicador = indicador_repository.get_by_id(
        request_indicador.id)
    resultados = []

    unidad = Unidad.porcentaje if len(
        indicador.sensores) > 1 else Unidad.absoluto

    for id_sensor, mediciones in map(lambda s: (s.id, _get_mediciones(s, request_indicador)), indicador.sensores):
        resultados.append(IndicadorResult(
            id_sensor, mediciones.sum()/len(mediciones), unidad))

    return resultados
