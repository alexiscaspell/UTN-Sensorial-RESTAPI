from apps.models.tarea_programada import TareaProgramada
from apps.utils.logger_util import get_logger
from apps.repositories.tablero_repository import get_tablero_by_reporte
from apps.models.tablero import Tablero
from apps.models.objetivo import Objetivo,ObjetivoResult
from apps.services.objetivo_service import procesar_objetivo_actual
from apps.models.grafico import GraficoObjetivo
import apps.utils.file_util as fu
from PyPDF2 import PdfFileMerger


logger = get_logger(__name__)


def generar_reporte(tarea:TareaProgramada,id_reporte:str):
    tablero = get_tablero_by_reporte(id_reporte)

    reporte_bytes = _tablero_to_pdf(tablero)

    return True,[reporte_bytes]

def _tablero_to_pdf(tablero:Tablero)->bytes:

    paths_graficos = []

    path_graficos="files/graficos"

    fu.make_directory_if_not_exists(path_graficos)

    for o in tablero.objetivos:
        grafico:GraficoObjetivo = GraficoObjetivo.from_dict({
            "nombre": o.nombre,
            "extension":"pdf",
            "nombre_archivo":fu.path_join(path_graficos,o.nombre.strip())
        })

        grafico.calcular([o,procesar_objetivo_actual(tablero.id,o)])
        grafico.generar_grafico()

        paths_graficos.append(grafico.get_path_completo())



    path_pdf = f"files/{''.join(tablero.nombre.split())}.pdf"
    merger = PdfFileMerger()

    for pdf in paths_graficos:
        merger.append(pdf)

    merger.write(path_pdf)
    merger.close()

    # fu.zip_file(path_graficos,path_zip)

    for p in paths_graficos:
        fu.delete_file(p)

    with open(path_pdf,"rb") as f:
        bytes_pdf =  f.read()

    fu.delete_file(path_pdf)

    return bytes_pdf


def _reporte_dummy(tarea:TareaProgramada,un_path_archivo):
    with open(un_path_archivo,"rb") as f:
        file_bytes = f.read()

    return True,["Every day is friday...",file_bytes]


def evaluar(expresion:str,*args):
    return eval(expresion,globals(),{"args":args})