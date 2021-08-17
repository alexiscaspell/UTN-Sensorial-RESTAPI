from apps.models.sensor import Sensor
from typing import List
from apps.repositories import tablero_repository


def get_all() -> List[Sensor]:
    return tablero_repository.get_all()