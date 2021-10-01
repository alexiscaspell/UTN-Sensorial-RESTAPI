from apps.models.app_model import AppModel,model_metadata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Tuple,Dict


@model_metadata({})
class Email(AppModel):
    def __init__(self,email_spec:Dict):
        self.de = email_spec["de"]
        self.usuario = email_spec.get("usuario",self.de)
        self.contrasenia = email_spec["contrasenia"]
        self.para = email_spec["para"]
        self.encabezado = email_spec["encabezado"]
        self.cuerpo = email_spec.get("cuerpo","")
        self.cuerpo_html = email_spec.get("cuerpo_html",None)
        self.copia = email_spec.get("copia",[])
        self.adjuntos = email_spec.get("adjuntos",[])

@model_metadata({})
class MailTemplate(AppModel):
    def __init__(self,template_spec:Dict):
        self.encabezado = template_spec["encabezado"]
        self.cuerpo = template_spec["cuerpo"]
        self.cuerpo_html = template_spec.get("cuerpo_html",None)
        self.adjuntos = template_spec.get("adjuntos",[])
