from datetime import datetime
from typing import Dict
from apps.models.app_model import AppModel, model_metadata
from apps.models.indicador import Indicador
from apps.models.objetivo import Objetivo
from apps.models.reporte import Reporte
from apps.models.sensor import Sensor


@model_metadata({"indicadores": Indicador, "objetivos": Objetivo, "reportes": Reporte, "fecha_creacion": datetime})
class Tablero(AppModel):
    def __init__(self, tablero_spec: Dict):
        self.id = tablero_spec.get("id", None)
        self.nombre = tablero_spec["nombre"]
        self.descripcion = tablero_spec.get("descripcion", "")
        self.fecha_creacion = tablero_spec.get("fecha_creacion", datetime.now())
        self.reportes = tablero_spec.get("reportes", [])
        self.objetivos = tablero_spec.get("objetivos", [])
        self.indicadores = tablero_spec.get("indicadores", [])
