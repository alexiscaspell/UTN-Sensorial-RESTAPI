from apps.models.app_model import AppModel,model_metadata
from typing import Dict,List
from apps.models.receptor_estado import ReceptorDeEstado,StatusTarea
from apps.models.email import MailTemplate
from importlib import import_module

@model_metadata({})
class ModuloExterno(AppModel):
    def __init__(self, modulo_spec):
        self.nombre_funcion = modulo_spec["funcion"]
        self.path = modulo_spec["modulo"]

        self.nombre_modulo_entero = self.path_a_modulo(self.path)
        self.nombre_modulo = self.nombre_modulo_entero.split(".").pop()
        self.carpeta = self.nombre_modulo_entero.replace(f".{self.nombre_modulo}","").replace(self.nombre_modulo,"")

        self.modulo = import_module(self.nombre_modulo_entero)
        self.funcion = self.get_funcion(self.nombre_funcion) if self.nombre_funcion else None
        self.argumentos = modulo_spec.get("argumentos",[])

    def path_a_modulo(self,path):
        #ESTO ES PORQUE ME REMPLAZA POR . LA PRIMERA /
        path_relativo = str(path)[1:] if str(path).startswith("/") else str(path)

        return path_relativo.replace("/",".").replace(".py","")

    def get_funcion(self,nombre_funcion:str=None):
        '''Retorna la funcion del modulo por nombre, si no se le pasa ninguno retorna funcion'''
        return getattr(self.modulo,nombre_funcion if nombre_funcion else self.nombre_funcion)

    def contiene_funcion(self,nombre_funcion:str):
        return getattr(self.modulo,nombre_funcion,False)
    
    def to_dict(self):
        return {
            "modulo":self.path,
            "funcion":self.nombre_funcion,
            "argumentos":self.argumentos
        }

@model_metadata({"receptores_estado":ReceptorDeEstado,"modulo_externo":ModuloExterno})
class TareaProgramada(AppModel):
    def __init__(self,tarea_programada_spec:Dict):
        self.cron = tarea_programada_spec["cron"]
        self.receptores_estado = tarea_programada_spec["receptores_estado"]
        self.id = tarea_programada_spec["id"]
        self.modulo_externo = tarea_programada_spec["modulo_externo"]
        self.activa = tarea_programada_spec.get("activa",True)

    def obtener_receptor(self,status:StatusTarea):
        return list(filter(lambda r:r.status.value==status.value,self.receptores_estado))[0]