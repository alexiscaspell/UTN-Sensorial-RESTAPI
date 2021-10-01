import json
import apps.configs.configuration as conf
from typing import List,Dict
from datetime import date

from apps.configs.vars import Vars
from apps.models.reporte import Reporte
from apps.models.tarea_programada import TareaProgramada,StatusTarea
from apps.models.receptor_estado import ReceptorDeEstado
from apps.utils.system_util import path_join
from apps.models.exception import AppException
from apps.utils.logger_util import get_logger
import apps.utils.scheduler_util as scheduler_util
from apps.services.mail_service import enviar_mail
from apps.repositories import tablero_repository



_sched = scheduler_util.crear_scheduler()

_ARCHIVO_CONFIG="config_tareas.json"

logger = get_logger(__name__)

def _funcion_vacia():
    print("f vacia")

def _funcion_wrapper(*args):
    tarea = list(args).pop(0)

    if not tarea.activa:
        return

    funcion_eval = tarea.modulo_externo.get_funcion("evaluar") if tarea.modulo_externo.contiene_funcion("evaluar") else lambda a,t: eval

    args = [tarea]+[funcion_eval(a,tarea) for a in tarea.modulo_externo.argumentos]

    logger.info(f"EJECUTANDO TAREA {tarea.id} ...")

    success,results = tarea.modulo_externo.get_funcion()(*args)

    status_tarea = StatusTarea.ok if success else StatusTarea.failed

    logger.info(f"TAREA {tarea.id} TERMINADA CON STATUS: {status_tarea}")

    receptor = tarea.obtener_receptor(status_tarea)

    if receptor.activo:
        logger.info(f"ARMANDO MAIL ...")

        #CLONE
        receptor = ReceptorDeEstado.from_dict(receptor.to_dict())

        receptor_parameters = [date.today(),status_tarea.value]+list(results)

        funcion_eval = tarea.modulo_externo.get_funcion("evaluar") if tarea.modulo_externo.contiene_funcion("evaluar") else lambda a,t: eval

        receptor.actualizar_template(funcion_eval,*receptor_parameters)

        logger.info(f"ENVIANDO MAIL ...")

        enviar_mail(receptor)

        logger.info(f"MAIL ENVIADO.")


def _crear_cron_tarea(tarea:TareaProgramada):
    '''
    Crea el cron correspondiente a la tarea programada
    '''
    funcion_eval = tarea.modulo_externo.get_funcion("evaluar") if tarea.modulo_externo.contiene_funcion("evaluar") else lambda a,t: eval

    job = scheduler_util.agregar_job(_sched, _funcion_vacia, tarea.cron,tarea.id)
    job.args = [tarea]+tarea.modulo_externo.argumentos
    job.func = _funcion_wrapper

def _eliminar_cron_tarea(id_tarea:str):
    '''
    Elimina el cron correspondiente a la tarea programada
    '''
    scheduler_util.remover_job(_sched,id_tarea)

def ejecutar_tarea(id_tarea:str,force_run=False):
    '''
    Ejecuta la tarea por id
    '''
    activa=False

    if force_run:
        tarea = get_tarea(id_tarea)
        activa = tarea.activa
        actualizar_atributos_tarea(id_tarea,{"activa":True})

    scheduler_util.ejecutar_job(_sched,id_tarea)

    if force_run:
        actualizar_atributos_tarea(id_tarea,{"activa":activa})

def get_tarea(id_tarea:str):
    '''
    Retorna una tareas por id
    '''
    return list(filter(lambda t:t.id==id_tarea,get_tareas()))[0]

def get_tareas():
    '''
    Retorna  la lista de tareas programadas
    '''
    ruta_config = path_join(conf.get(Vars.DIRECTORIO_FILES),_ARCHIVO_CONFIG)

    with open(ruta_config,"r") as f:
        tareas_programadas = json.load(f)

    return [TareaProgramada.from_dict(t) for t in tareas_programadas]

def actualizar_atributos_tarea(id_tarea:str,atributos_nuevos:Dict):
    '''
    Modifica los atributos pasados en el diccionario de la tarea ya existente con id: id_tarea
    '''
    tarea_a_actualizar = get_tarea(id_tarea)
    tarea_a_actualizar_dict = tarea_a_actualizar.to_dict()

    tarea_a_actualizar_dict.update(atributos_nuevos)

    eliminar_tarea(id_tarea)

    agregar_tarea(TareaProgramada.from_dict(tarea_a_actualizar_dict))

    return tarea_a_actualizar_dict

    
def save_tareas_programadas(tareas_programadas:List[TareaProgramada]):
    '''
    Retorna  la lista de tareas programadas
    '''
    ruta_config = path_join(conf.get(Vars.DIRECTORIO_FILES),_ARCHIVO_CONFIG)

    with open(ruta_config,"w") as f:
        tareas_programadas_dict=[t.to_dict() for t in tareas_programadas]
        json.dump(tareas_programadas_dict,f)

def agregar_tarea(tarea:TareaProgramada):
    '''
    Crea el cron con la tarea programada y persiste la config
    '''
    ruta_config = path_join(conf.get(Vars.DIRECTORIO_FILES),_ARCHIVO_CONFIG)

    tareas_programadas = get_tareas()

    if(any(tarea.id==t.id for t in tareas_programadas)):
        raise AppException("TAREA_EXISTENTE",f"La tarea con el id {tarea.id} ya existe")

    _crear_cron_tarea(tarea)

    tareas_programadas.append(tarea)

    save_tareas_programadas(tareas_programadas)


def eliminar_tarea(id_tarea:str):
    '''
    Borra la tarea correspondiente a id_tarea
    '''
    tareas_programadas = get_tareas()

    tareas_programadas = list(filter(lambda t:t.id!=id_tarea,tareas_programadas))

    _eliminar_cron_tarea(id_tarea)

    save_tareas_programadas(tareas_programadas)

def iniciar_proceso_automatico():
    '''
    Inicia el scheduler con las tareas configuradas
    '''
    tareas = get_tareas()

    logger.info(f'Iniciando proceso automatico ...')

    for tarea in tareas:
        _crear_cron_tarea(tarea)

    scheduler_util.inciar_scheduler(_sched)

def cargar_reportes():
    try:
        reportes = tablero_repository.get_all_reportes()

        for reporte in reportes:
            agregar_tarea(reporte.to_tarea_programada())
            
    except Exception as e:
        logger.error("Error al agregar reporte:")
        logger.error(reporte.to_dict() if reporte else None)
        logger.error(e)

def cargar_reporte(reporte:Reporte):
    try:
        agregar_tarea(reporte.to_tarea_programada())
            
    except Exception as e:
        logger.error("Error al agregar reporte:")
        logger.error(reporte.to_dict())
        logger.error(e)