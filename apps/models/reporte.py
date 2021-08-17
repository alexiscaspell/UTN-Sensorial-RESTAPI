from typing import Dict
from apps.models.app_model import AppModel,model_metadata
from apps.models.indicador import Indicador
from apps.models.objetivo import Objetivo


@model_metadata({"indicadores":Indicador,"objetivos":Objetivo})
class Reporte(AppModel):
    def __init__(self, reporte_spec: Dict):
        self.id = reporte_spec.get("id", None)
        self.nombre = reporte_spec["nombre"]
        self.path_archivo = reporte_spec.get("path_archivo",None)
        self.objetivos = reporte_spec.get("objetivos",[])
        self.indicadores = reporte_spec.get("indicadores",[])
        self.config = reporte_spec.get("config",dict())

    def cargar_config_reporte(self,config:Dict):
        self.config = config

    def generar_reporte(self):
        raise NotImplementedError("Funcion generar reporte no implementada")