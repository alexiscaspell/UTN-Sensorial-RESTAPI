from typing import Dict
from apps.models.app_model import AppModel,model_metadata
from apps.models.sensor import Sensor


@model_metadata({"sensor":Sensor})
class Medicion(AppModel):
    def __init__(self, medicion_spec: Dict):
        self.id = medicion_spec.get("id", None)
        self.nombre = medicion_spec["nombre"]
        self.valor = medicion_spec["valor"]
        self.sensor = medicion_spec["sensor"]
        self.unidad = medicion_spec["unidad"]