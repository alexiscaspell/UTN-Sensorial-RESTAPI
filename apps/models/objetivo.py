from datetime import datetime
from typing import Dict,List
from apps.models.app_model import AppModel,model_metadata
from apps.models.indicador import Indicador
from enum import Enum

class ObjetivoStatus(Enum):
    pendiente = "pendiente"
    no_cumplido = "no_cumplido"
    cumplido = "cumplido"
@model_metadata({"status":ObjetivoStatus})
class ObjetivoResult(AppModel):
    def __init__(self,result_spec):
        self.id_objetivo = result_spec["id_objetivo"]
        self.status = result_spec["status"]

@model_metadata({"fecha_incial":datetime,"fecha_final":datetime})
class Objetivo(AppModel):
    def __init__(self, objetivo_spec: Dict):
        self.id = objetivo_spec.get("id", None)
        self.nombre = objetivo_spec["nombre"]
        self.descripcion = objetivo_spec.get("descripcion","")
        self.fecha_inicial = objetivo_spec.get("fecha_inicial",None)
        self.fecha_final = objetivo_spec.get("fecha_final",None)

        self.id_indicador = objetivo_spec["id_indicador"]
        self.nombre_indicador = objetivo_spec["nombre_indicador"]

        self.valor = objetivo_spec.get("valor",None)
        self.funcion = None

    def evaluar(self,params:List[object]):
        raise NotImplementedError("Funcion evaluar no implementada")