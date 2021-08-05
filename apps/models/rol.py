from datetime import datetime
from typing import Dict
from apps.models.app_model import AppModel,model_metadata


@model_metadata({})
class Rol(AppModel):
    def __init__(self, rol_spec: Dict):
        self.id = rol_spec.get("id", None)
        self.nombre = rol_spec["nombre"]
        self.permisos = rol_spec["permisos"]

    def puede_acceder(self,uri:str):
        return uri in self.permisos