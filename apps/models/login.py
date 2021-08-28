from datetime import datetime
from typing import Dict
from apps.models.app_model import AppModel,model_metadata


@model_metadata({})
class Login(AppModel):
    def __init__(self, login_spec: Dict):
        self.id = login_spec.get("id", None)
        self.user = login_spec["user"]
        self.password = login_spec["password"]
        self.habilitado = login_spec.get("habilitado",True)
        self.ultimo_acceso = login_spec.get("ultimo_acceso",datetime.now())

    def es_valido(self,user:str,password:str)->bool:
        return self.user==user and self.password==password

    def actualizar_ultimo_acceso(self,fecha:datetime):
        self.ultimo_acceso = fecha