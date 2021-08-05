from datetime import datetime
from typing import Dict
from apps.models.app_model import AppModel,model_metadata


@model_metadata({})
class Ejemplo(AppModel):
    def __init__(self, ejemplo_spec: Dict):
        self.id = ejemplo_spec.get("id", None)
        self.email = ejemplo_spec["email"]
        self.nombre = ejemplo_spec["nombre"]