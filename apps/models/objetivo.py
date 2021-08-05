from typing import Dict,List
from apps.models.app_model import AppModel,model_metadata
from apps.models.indicador import Indicador


@model_metadata({"indicadores":Indicador})
class Objetivo(AppModel):
    def __init__(self, objetivo_spec: Dict):
        self.id = objetivo_spec.get("id", None)
        self.nombre = objetivo_spec["nombre"]
        self.indicadores = objetivo_spec["indicadores"]
        self.funcion = None

    def evaluar(self,params:List[object]):
        raise NotImplementedError("Funcion evaluar no implementada")