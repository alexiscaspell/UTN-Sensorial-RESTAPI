from typing import Dict
from apps.models.app_model import AppModel,model_metadata
from apps.models.sensor import Sensor


@model_metadata({"sensores":Sensor})
class Mensurable(AppModel):
    def __init__(self, mensurable_spec: Dict):
        self.id = mensurable_spec.get("id", None)
        self.nombre = mensurable_spec["nombre"]
        self.cluster = mensurable_spec["cluster"]
        self.sensores = mensurable_spec.get("sensores",[])