from typing import Dict,List
from apps.models.app_model import AppModel,model_metadata


@model_metadata({})
class Indicador(AppModel):
    def __init__(self, indicador_spec: Dict):
        self.id = indicador_spec.get("id", None)
        self.nombre = indicador_spec["nombre"]
        self.parametros = indicador_spec.get("parametros",[])
        self.funcion = None
        self.unidad = indicador_spec["unidad"]

    def calcular(self,params:List[object])->float:
        raise NotImplementedError("Funcion para calcular el indicador no implementada")
    
    def obtener_sensor(self):
        raise NotImplementedError("Funcion obtener sensor no implementada")