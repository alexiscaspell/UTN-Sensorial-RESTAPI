from datetime import date, datetime, timedelta
from logging import disable
from typing import Dict, List
from apps.models.app_model import AppModel, model_metadata
from apps.models.sensor import Sensor
from apps.models.medicion import Medicion
from enum import Enum


class UnidadValor(Enum):
    porcentaje = "porcentaje"
    absoluto = "absoluto"


class UnidadTiempo(Enum):
    hora = "hora"
    dia = "dia"
    semana = "semana"
    mes = "mes"
    anio = "anio"


@model_metadata({"unidad": UnidadValor,"valores":Medicion})
class IndicadorResult(AppModel):
    def __init__(self, id_sensor: str, valores: List[float], unidad: UnidadValor):
        self.id_sensor = id_sensor
        self.valores = valores
        self.unidad = unidad
    
    def to_json(self):
        return {
            "id_sensor":self.id_sensor,
            "unidad":self.unidad.value,
            "valores":[v.to_json() for v in self.valores]
        }

@model_metadata({"desde": datetime, "hasta": datetime, "unidad": UnidadTiempo})
class IndicadorHistoricoRequest(AppModel):
    def __init__(self, request_spec: Dict):
        self.id = request_spec["id"]
        self.id_tablero = request_spec["id_tablero"]
        self.granularidad = request_spec.get("granularidad", 1)
        self.unidad = request_spec.get("unidad", UnidadTiempo.mes)
        self.hasta = request_spec.get("hasta", datetime.now())
        self.desde = request_spec.get("desde", self.hasta-timedelta(days=1))


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


@model_metadata({"tipo": TipoIndicador,"sensores":Sensor})
class Indicador(AppModel):
    def __init__(self, indicador_spec: Dict):
        self.id = indicador_spec.get("id", None)
        self.nombre = indicador_spec["nombre"]
        self.sensores = indicador_spec["sensores"]
        self.tipo = indicador_spec["tipo"]
        self.limite_superior = indicador_spec.get("limite_superior", None)
        self.limite_superior = indicador_spec.get("limite_inferior", None)

        self.parametros = indicador_spec.get("parametros", [])
        self.funcion = None