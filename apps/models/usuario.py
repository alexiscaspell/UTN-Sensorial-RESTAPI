from datetime import datetime
from typing import Dict

from apps.models.app_model import AppModel, model_metadata
from apps.models.rol import Rol
from apps.models.tablero import Tablero


@model_metadata({"rol":Rol,"tableros":Tablero})
class Usuario(AppModel):
    def __init__(self, user_spec: Dict):
        self.id = user_spec.get("id", None)
        self.nombre = user_spec["nombre"]
        self.rol = user_spec.get("rol",Rol.user)
        self.mail = user_spec["mail"]
        self.password = user_spec["password"]
        self.fecha_creacion = user_spec.get("fecha_creacion",datetime.now())
        self.ultimo_login = user_spec["ultimo_login"]
        self.tableros = user_spec.get("tableros",[])