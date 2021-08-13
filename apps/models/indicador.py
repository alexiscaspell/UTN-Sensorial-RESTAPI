from typing import Dict, List
from apps.models.app_model import AppModel, model_metadata
from apps.models.sensor import Sensor
from enum import Enum


class Unidad(Enum):
    porcentaje = "porcentaje"
    absoluto = "absoluto"


@model_metadata({"unidad": Unidad})
class IndicadorResult(AppModel):
    def __init__(self, id_sensor: str, valor: float, unidad: Unidad):
        self.id_sensor = id_sensor
        self.valor = valor
        self.unidad = unidad


class IndicadorRequest(AppModel):
    def __init__(self, request_spec: Dict):
        self.id = request_spec["id"]
        self.muestras = request_spec.get("muestras", None)
        self.desde = request_spec.get("desde", None)
        self.hasta = request_spec.get("hasta", None)


@model_metadata({"sensores": Sensor})
class Indicador(AppModel):
    def __init__(self, indicador_spec: Dict):
        self.id = indicador_spec.get("id", None)
        self.nombre = indicador_spec["nombre"]
        self.sensores = indicador_spec["sensores"]
        self.tipo = indicador_spec["tipo"]
        self.limite_superior = indicador_spec["limite_superior"]
        self.limite_superior = indicador_spec.get("limite_inferior", None)

        self.parametros = indicador_spec.get("parametros", [])
        self.funcion = None

    def calcular(self, params: List[object]) -> float:
        raise NotImplementedError(
            "Funcion para calcular el indicador no implementada")

    def obtener_sensor(self):
        raise NotImplementedError("Funcion obtener sensor no implementada")
