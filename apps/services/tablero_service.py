from apps.models.sensor import Sensor
from typing import List
from apps.repositories import tablero_repository
from apps.models.reporte import Reporte
from apps.services import tasks_service as tasks_service

def guardar_reporte(id_tablero:str,reporte:Reporte)->Reporte:
    reporte = tablero_repository.add_reporte(id_tablero,reporte)
    tasks_service.cargar_reporte(reporte)
    return reporte

def borrar_reporte(id_tablero:str,id_reporte:str):
    tablero_repository.delete_reporte(id_tablero,id_reporte)
    tasks_service.eliminar_tarea(id_reporte)


def get_all() -> List[Sensor]:
    return tablero_repository.get_all()