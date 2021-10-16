from typing import Dict
from apps.models.app_model import AppModel,model_metadata


@model_metadata({})
class Sensor(AppModel):
    def __init__(self, sensor_spec: Dict):
        self.id = sensor_spec.get("id", None)
        self.nombre = sensor_spec["nombre"]
        self.tipo = sensor_spec["tipo"]
        self.MAC = sensor_spec.get("MAC",None)