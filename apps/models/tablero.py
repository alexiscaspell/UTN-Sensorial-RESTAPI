from typing import Dict
from apps.models.app_model import AppModel,model_metadata
from apps.models.indicador import Indicador


@model_metadata({"indicadores":Indicador})
class Tablero(AppModel):
    def __init__(self, tablero_spec: Dict):
        self.id = tablero_spec.get("id", None)
        self.nombre = tablero_spec["nombre"]
        self.indicadores = tablero_spec.get("indicadores",[])