from datetime import datetime
from typing import Dict, List
from apps.models.objetivo import Objetivo,ObjetivoResult, ObjetivoStatus
from apps.repositories import tablero_repository
from apps.services.indicador_service import get_mediciones,get_indicador
from apps.utils.logger_util import get_logger

logger = get_logger(__name__)

def get_objetivo(id_tablero,id_objetivo)->Objetivo:
    return tablero_repository.get_objetivo(id_tablero,id_objetivo)

def procesar_objetivo(id_tablero:str,id_objetivo:str) -> ObjetivoResult:
    logger.info(f"PROCESANDO OBJETIVO {id_tablero}/{id_objetivo} ...")

    objetivo:Objetivo = get_objetivo(id_tablero, id_objetivo)

    objetivo_result = procesar_objetivo_actual(id_tablero,objetivo)

    logger.info(f"RESULTADO: {objetivo_result.to_dict()}")

    return objetivo_result



def procesar_objetivo_actual(id_tablero:str,objetivo:Objetivo) -> ObjetivoResult:
    indicador = get_indicador(id_tablero,objetivo.id_indicador)
    id_objetivo = objetivo.id

    valor = objetivo.valor_calculado

    if valor is None:
        counts = []

        for sensor in indicador.sensores:
            mediciones = get_mediciones(sensor,desde=objetivo.fecha_inicial, hasta=objetivo.fecha_final)

            count=0

            for m in mediciones:
                if m.valor<= indicador.limite_superior:
                    if indicador.limite_inferior is None or m.valor>=indicador.limite_inferior:
                        count+=1 

            counts.append({"sensor":sensor.id,"contador":count,"mediciones":len(mediciones)})

        mediciones_totales=0
        contador_total=0

        for c in counts:
            contador_total+=c["contador"]
            mediciones_totales+=c["mediciones"]

        valor = contador_total/max(mediciones_totales,1)*100

    status = objetivo.evaluar(valor)

    if status!=ObjetivoStatus.pendiente:
        objetivo.valor_calculado = valor
        tablero_repository.save_objetivo(id_tablero,objetivo)

    return ObjetivoResult.from_dict({"id_objetivo":id_objetivo,"status":status,"valor":valor,"valor_esperado":objetivo.valor})
