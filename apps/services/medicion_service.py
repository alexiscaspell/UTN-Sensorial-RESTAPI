from typing import List

from apps.models.medicion import MedicionRaspberry
from apps.repositories import medicion_repository as medicion_repository


def guardar_mediciones(mediciones: List[MedicionRaspberry]):
    medicion_repository.guardar_varias([m.to_medicion() for m in mediciones])
