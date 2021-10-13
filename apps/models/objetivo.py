from datetime import datetime
from typing import Dict,List
from apps.models.app_model import AppModel,model_metadata
from apps.models.indicador import Indicador
from enum import Enum
from apps.models.exception import ObjetivoInvalidoException

class ObjetivoStatus(Enum):
    pendiente = "pendiente"
    no_cumplido = "no_cumplido"
    cumplido = "cumplido"
    
@model_metadata({"status":ObjetivoStatus})
class ObjetivoResult(AppModel):
    def __init__(self,result_spec):
        self.id_objetivo = result_spec["id_objetivo"]
        self.status = result_spec["status"]
        self.valor = result_spec.get("valor",None)
        self.valor_esperado = result_spec.get("valor_esperado",None)

    def to_dict(self):
        result = super().to_dict()
        result["valor"]=round(result["valor"],2)
        result["valor_esperado"]=round(result["valor_esperado"],2)
        return result

@model_metadata({"fecha_inicial":datetime,"fecha_final":datetime,"valor":float,"valor_calculado":float})
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
        self.valor_calculado = objetivo_spec.get("valor_calculado",None)
        self.funcion = None

    def to_dict(self):
        result = super().to_dict()
        result.pop("funcion",None)
        return result

    def to_bson():
        result = super().to_dict()
        result["valor"] = str(round(result["valor"],2)) if result["valor"] is not None else None
        result["valor_calculado"] = str(round(result["valor"],2)) if result["valor_calculado"] is not None else None

        return result




    def evaluar(self,valor:float)->ObjetivoStatus:
        if self.valor is None:
            raise ObjetivoInvalidoException(self.id)
        
        fecha_actual=datetime.now()

        status = ObjetivoStatus.cumplido if valor>=self.valor and fecha_actual>self.fecha_final else ObjetivoStatus.pendiente

        if datetime.now()> self.fecha_final and status==ObjetivoStatus.pendiente:
            status = ObjetivoStatus.no_cumplido

        return status
