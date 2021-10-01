from typing import Callable

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime

_MAX_HILOS_POR_JOB = 1


def crear_scheduler() -> BackgroundScheduler:
    '''
    Crea el scheduler que se va a utilizar 
    '''
    return BackgroundScheduler()


def parar_scheduler(scheduler: BackgroundScheduler):
    '''
    Crea el scheduler que se va a utilizar 
    '''
    scheduler.shutdown(wait=False)


def inciar_scheduler(scheduler: BackgroundScheduler):
    '''
    Crea el scheduler que se va a utilizar 
    '''
    scheduler.start()

def ejecutar_job(scheduler: BackgroundScheduler,id_job: str):
    '''
    Ejecuta el job con id=id_job
    '''
    scheduler.get_job(job_id =id_job).modify(next_run_time=datetime.datetime.now())



def remover_job(scheduler: BackgroundScheduler, id: str) -> Job:
    '''
    Crea el scheduler que se va a utilizar 
    '''
    return scheduler.remove_job(id)


def agregar_job(scheduler: BackgroundScheduler, funcion: Callable, cron: str,
                id: str) -> Job:
    '''
    Agrega un job al scheduler mediante una funcion y un cron
    '''
    job = scheduler.add_job(funcion, CronTrigger.from_crontab(cron), id=id)
    job.modify(max_instances=_MAX_HILOS_POR_JOB)

    return job
