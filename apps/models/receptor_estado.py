from apps.models.app_model import AppModel,model_metadata
from apps.models.email import MailTemplate
from typing import Dict,List
from enum import Enum

class StatusTarea(Enum):
    ok = "ok"
    failed = "failed"
    
@model_metadata({"template":MailTemplate})
class ReceptorDeEstado(AppModel):
    def __init__(self,receptor_spec:Dict):
        self.status = StatusTarea(receptor_spec["status"])
        self.destinatarios = receptor_spec["destinatarios"]
        self.en_copia = receptor_spec.get("en_copia",[])
        self.template = receptor_spec["template"]
        self.activo = receptor_spec.get("activo",True)

    def actualizar_template(self,funcion_eval,*args):
        self.template.encabezado = funcion_eval(self.template.encabezado,*args)
        self.template.cuerpo = funcion_eval(self.template.cuerpo,*args) if self.template.cuerpo is not None and self.template.cuerpo!="" else ""
        self.template.cuerpo_html = funcion_eval(self.template.cuerpo_html,*args) if self.template.cuerpo_html is not None and self.template.cuerpo_html!="" else ""
        self.template.adjuntos = [tuple(funcion_eval(adjunto,*args)) for adjunto in self.template.adjuntos]