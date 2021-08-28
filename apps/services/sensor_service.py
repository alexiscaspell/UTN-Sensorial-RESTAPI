from apps.models.sensor import Sensor
from typing import List
from apps.repositories import sensor_repository


def get_all() -> List[Sensor]:
    return sensor_repository.get_all()

def guardar(sensor:Sensor):
    sensor_repository.save(sensor)
