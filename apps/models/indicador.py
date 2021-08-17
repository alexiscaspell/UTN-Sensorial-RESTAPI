from datetime import date, datetime, timedelta
from logging import disable
from typing import Dict, List
from apps.models.app_model import AppModel, model_metadata
from apps.models.sensor import Sensor
from enum import Enum


class UnidadValor(Enum):
    porcentaje = "porcentaje"
    absoluto = "absoluto"


class UnidadTiempo(Enum):
    hora = "hora"
    dia = "dia"
    semana = "semana"
    mes = "mes"


@model_metadata({"unidad": UnidadValor})
class IndicadorResult(AppModel):
    def __init__(self, id_sensor: str, valores: List[float], unidad: UnidadValor):
        self.id_sensor = id_sensor
        self.valores = valores
        self.unidad = unidad


@model_metadata({"desde": datetime, "hasta": datetime, "unidad": UnidadTiempo})
class IndicadorHistoricoRequest(AppModel):
    def __init__(self, request_spec: Dict):
        self.id = request_spec["id"]
        self.id_tablero = request_spec["id_tablero"]
        self.granularidad = request_spec.get("granularidad", 1)
        self.unidad = request_spec.get("unidad", UnidadTiempo.mes)
        self.hasta = request_spec.get("hasta", datetime.now())
        self.desde = request_spec.get("desde", self.desde-timedelta(days=1))


class IndicadorRequest(AppModel):
    def __init__(self, request_spec: Dict):
        self.id = request_spec["id"]
        self.id_tablero = request_spec["id_tablero"]
        self.muestras = request_spec.get("muestras", 1)


class TipoIndicador(Enum):
    produccion = "produccion"
    temperatura = "temperatura"
    humedad = "humedad"
    calidad_del_aire = "calidad_del_aire"


@model_metadata({"tipo": TipoIndicador})
class Indicador(AppModel):
    def __init__(self, indicador_spec: Dict):
        self.id = indicador_spec.get("id", None)
        self.nombre = indicador_spec["nombre"]
        self.id_sensores = indicador_spec["id_sensores"]
        self.tipo = indicador_spec["tipo"]
        self.limite_superior = indicador_spec.get("limite_superior", None)
        self.limite_superior = indicador_spec.get("limite_inferior", None)

        self.parametros = indicador_spec.get("parametros", [])
        self.funcion = None