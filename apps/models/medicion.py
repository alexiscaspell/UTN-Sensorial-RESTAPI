from typing import Dict

from apps.models.app_model import AppModel, model_metadata
from apps.models.sensor import Sensor
from datetime import datetime


@model_metadata({"fecha":datetime})
class Medicion(AppModel):
    def __init__(self, medicion_spec: Dict):
        self.id = medicion_spec.get("id", None)
        self.valor = medicion_spec["valor"]
        self.id_sensor = medicion_spec["id_sensor"]
        self.tipo_sensor = medicion_spec["tipo_sensor"]
        self.unidad = medicion_spec.get("unidad", None)
        self.fecha = medicion_spec.get("fecha", datetime.now())


@model_metadata({})
class MedicionRaspberry(AppModel):
    def __init__(self, medicion_spec):
        self.creation_date = medicion_spec["creation_date"]
        self.mac = medicion_spec["mac"]
        self.unit = medicion_spec["unit"]
        self.sensor_type = medicion_spec["sensor_type"]
        self.raspberry_uuid = medicion_spec["raspberry_uuid"]
        self.value = medicion_spec["value"]

    def to_medicion(self) -> Medicion:
        Medicion.from_dict({
            "valor": self.value,
            "id_sensor": self.mac,
            "tipo_sensor": self.sensor_type,
            "unidad": self.unit,
            "fecha": self.creation_date
        })
