from datetime import datetime
from typing import Dict, List
from apps.models.objetivo import Objetivo,ObjetivoResult, ObjetivoStatus
from apps.repositories import tablero_repository
from apps.services.indicador_service import get_mediciones,get_indicador

def get_objetivo(id_tablero,id_objetivo)->Objetivo:
    return tablero_repository.get_objetivo(id_tablero,id_objetivo)

def procesar_objetivo(id_tablero:str,id_objetivo:str) -> ObjetivoResult:
    objetivo:Objetivo = get_objetivo(id_tablero, id_objetivo)
    indicador = get_indicador(id_tablero,objetivo.id_indicador)

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

    status = ObjetivoStatus.cumplido if valor>=float(objetivo.valor) else ObjetivoStatus.pendiente

    if datetime.now()> objetivo.fecha_final and status==ObjetivoStatus.pendiente:
        status = ObjetivoStatus.no_cumplido

    return ObjetivoResult.from_dict({"id_objetivo":id_objetivo,"status":status,"valor":valor,"valor_esperado":objetivo.valor})
