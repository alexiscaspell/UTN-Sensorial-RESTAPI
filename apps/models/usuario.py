from apps.models.rol import Rol
from typing import Dict
from apps.models.app_model import AppModel,model_metadata
from apps.models.rol import Rol
from apps.models.login import Login
from apps.models.tablero import Tablero


@model_metadata({"roles":Rol,"login":Login,"tableros":Tablero})
class Usuario(AppModel):
    def __init__(self, user_spec: Dict):
        self.id = user_spec.get("id", None)
        self.nombre = user_spec["nombre"]
        self.roles = user_spec.get("roles",[])
        self.login = user_spec["login"]
        self.telefono = user_spec["telefono"]
        self.tableros = user_spec.get("tableros",[])