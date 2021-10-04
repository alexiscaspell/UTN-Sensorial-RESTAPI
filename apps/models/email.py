from apps.models.app_model import AppModel,model_metadata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Tuple,Dict

@model_metadata({})
class Adjunto(AppModel):
    def __init__(self,data):
        if not isinstance(data,tuple):
            raise RuntimeError("Adjunto debe ser una tupla con nombre,bytes")

        self.nombre = data[0]

        if isinstance(data[1],str):
            with open(data[1],"rb") as f:
                self.bytes = f.read()
        else:
            self.bytes = data[1]

    def raw(self):
        return (self.nombre,self.bytes)


@model_metadata({"adjuntos":Adjunto})
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
        self.adjuntos = email_spec.get("adjuntos", [])

        if isinstance(self.para,str):
            self.para = list(self.para.split(","))

        if isinstance(self.copia,str):
            self.copia = list(self.copia.split(","))

@model_metadata({})
class MailTemplate(AppModel):
    def __init__(self,template_spec:Dict):
        self.encabezado = template_spec["encabezado"]
        self.cuerpo = template_spec["cuerpo"]
        self.cuerpo_html = template_spec.get("cuerpo_html",None)
        self.adjuntos = template_spec.get("adjuntos",[])
