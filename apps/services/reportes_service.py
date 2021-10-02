from PyPDF2.generic import ObjectPrefix
from apps.models.tarea_programada import TareaProgramada
from apps.utils.logger_util import get_logger
from apps.repositories.tablero_repository import get_tablero_by_reporte
from apps.models.tablero import Tablero
from apps.models.objetivo import Objetivo, ObjetivoResult, ObjetivoStatus
from apps.services.objetivo_service import procesar_objetivo_actual
from apps.models.grafico import GraficoObjetivo
import apps.utils.file_util as fu
from PyPDF2 import PdfFileMerger, PdfFileReader


logger = get_logger(__name__)


def generar_reporte(tarea: TareaProgramada, id_reporte: str):
    tablero = get_tablero_by_reporte(id_reporte)

    reporte_pdf_path = _tablero_to_pdf(tablero)

    return True, [reporte_pdf_path]


def _tablero_to_pdf(tablero: Tablero) -> bytes:

    paths_graficos = []

    path_graficos = "files/graficos"

    fu.make_directory_if_not_exists(path_graficos)

    cumplidos = 0
    totales = len(tablero.objetivos)

    for objetivo in tablero.objetivos:
        objetivo_result = procesar_objetivo_actual(tablero.id, objetivo)

        if objetivo_result.status == ObjetivoStatus.cumplido:
            cumplidos += 1

        grafico = _procesar_grafico_objetivo(
            objetivo, objetivo_result, path_graficos)
        paths_graficos.append(grafico.get_path_completo())

    objetivo_dummy = Objetivo.from_dict({
        "nombre": "Objetivos totales",
        "id_indicador": "dummy",
        "nombre_indicador": "dummy",
        "objetivo": 0.75
    })

    objetivo_result_dummy = ObjetivoResult.from_dict({
        "id_objetivo": "dummy",
        "status": cumplidos/totales >= objetivo_dummy.objetivo if ObjetivoStatus.cumplido else ObjetivoStatus.no_cumplido,
        "valor": cumplidos/totales,
        "valor_esperado": objetivo_dummy.objetivo
    })

    path_graficos.append(_procesar_grafico_objetivo(objetivo_dummy,objetivo_result_dummy,path_graficos).get_path_completo())

    path_pdf = f"files/mergedfilesoutput.pdf"
    merger = PdfFileMerger()

    for p_path in paths_graficos:
        with open(p_path, "rb") as pdf:
            merger.append(PdfFileReader(pdf, "rb"))

    merger.write(path_pdf)
    merger.close()

    for p in paths_graficos:
        fu.delete_file(p)

    return path_pdf


def _procesar_grafico_objetivo(objetivo: Objetivo, objetivo_result: ObjetivoResult, path_graficos: str):
    grafico = GraficoObjetivo.from_dict({
        "nombre": objetivo.nombre,
        "extension": "pdf",
        "nombre_archivo": fu.path_join(path_graficos, objetivo.nombre.strip())
    })

    grafico.calcular([objetivo, objetivo_result])
    grafico.generar_grafico()

    return grafico


def _reporte_dummy(tarea: TareaProgramada, un_path_archivo):
    with open(un_path_archivo, "rb") as f:
        file_bytes = f.read()

    return True, ["Every day is friday...", file_bytes]


def evaluar(expresion: str, *args):
    return eval(expresion, globals(), {"args": args})
