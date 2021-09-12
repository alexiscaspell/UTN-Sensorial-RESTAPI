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
    horas_minutos = "horas_minutos"
    hora = "hora"
    dia = "dia"
    semana = "semana"
    mes = "mes"
    anio = "anio"


@model_metadata({"unidad": UnidadValor, "valores": Medicion, "unidad_tiempo": UnidadTiempo})
class IndicadorResult(AppModel):
    def __init__(self, id_sensor: str, valores: List[float], unidad: UnidadValor, unidad_tiempo: UnidadTiempo = UnidadTiempo.horas_minutos, nombre_sensor=""):
        self.id_sensor = id_sensor
        self.nombre_sensor = nombre_sensor
        self.valores = valores
        self.unidad = unidad
        self.unidad_tiempo = unidad_tiempo

    def _get_fecha_formateada(self, fecha: datetime):
        if self.unidad_tiempo == UnidadTiempo.hora:
            fecha = f"{fecha.day:02d} {fecha.hour:02d}"
        elif self.unidad_tiempo == UnidadTiempo.dia:
            fecha = f"{fecha.day:02d}-{fecha.month:02d}"
        elif self.unidad_tiempo == UnidadTiempo.semana:
            fecha = f"{fecha.day:02d}-{fecha.month:02d}"
        elif self.unidad_tiempo == UnidadTiempo.mes:
            fecha = f"{fecha.month:02d}-{fecha.year}"
        elif self.unidad_tiempo == UnidadTiempo.anio:
            fecha = f"{fecha.year}"
        elif self.unidad_tiempo == UnidadTiempo.horas_minutos:
            fecha = f"{fecha.hour:02d}:{fecha.minute:02d}:{fecha.second:02d}"

        return fecha

    def to_json(self):
        valores = list(reversed(self.valores))
        result = {
            "nombre_sensor": self.nombre_sensor,
            "unidad": self.unidad.value,
            "valores": [v.to_json() for v in valores]
        }
        for i, v in enumerate(result["valores"]):
            v["fecha"] = self._get_fecha_formateada(valores[i].fecha)

        return result


class IndicadorResultList:
    def __init__(self, resultados: List[IndicadorResult]):
        self.resultados = resultados
        pass

    def to_json(self):
        unidad = None if len(
            self.resultados) == 0 else self.resultados[0].unidad.value

        resultados_json = [r.to_json() for r in self.resultados]

        fechas = []
        for r in resultados_json:
            for v in r["valores"]:
                if v["fecha"] not in fechas:
                    fechas.append(v["fecha"])

        result = []

        for fecha in fechas:
            new_res = {"unidad": unidad, "fecha": fecha}

            for r in resultados_json:
                for v in r["valores"]:
                    if v["fecha"] == fecha:
                        new_res[r["nombre_sensor"]] = v["valor"]

            result.append(new_res)

        return result


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


@model_metadata({"tipo": TipoIndicador, "sensores": Sensor})
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
