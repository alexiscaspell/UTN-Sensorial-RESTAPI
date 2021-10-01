from re import split
from typing import Dict
from apps.models.app_model import AppModel, model_metadata
from apps.models.tarea_programada import TareaProgramada
from enum import Enum

class Dia(Enum):
    lunes = "Lunes"
    martes = "Martes"
    miercoles = "Miércoles"
    jueves = "Jueves"
    viernes = "Viernes"
    sabado = "Sábado"
    domingo = "Domingo"


@model_metadata({"dia": Dia})
class Reporte(AppModel):
    def __init__(self, reporte_spec: Dict):
        self.id = reporte_spec.get("id", None)
        self.nombre = reporte_spec["nombre"]
        self.descripcion = reporte_spec.get("descripcion", None)
        self.destinatarios = reporte_spec["destinatarios"]
        self.dia = reporte_spec["dia"]
        self.horario = reporte_spec["horario"]

    def to_tarea_programada(self) -> TareaProgramada:
        return TareaProgramada.from_dict({
            "cron": self._get_cron(),
            "receptores_estado": [{
                "status": "ok",
                "destinatarios": self.destinatarios,
                "template": {
                    "encabezado": "f'Reporte "+self.nombre+" {args[0].day:02d}/{args[0].month:02d}'",
                    "cuerpo": "f'Por la presente se envia el reporte "+self.nombre+" a la fecha de {args[0].day:02d}/{args[0].month:02d}/{args[0].year:02d}'",
                    "adjuntos": [
                        "(f'"+self.nombre +
                          "_{args[0].day:02d}_{args[0].month:02d}.zip',args[2])"
                    ]
                },
                "activo": True
            }],
            "id": self.id,
            "modulo_externo": {
                "modulo": "apps.services.reportes_service",
                "funcion": "generar_reporte",
                "argumentos": [
                    f"'{self.id}'"
                ]
            }
        })

    def _get_cron(self):
        if self.dia == Dia.lunes:
            dia_cron = "MON"
        elif self.dia == Dia.martes:
            dia_cron = "TUE"
        elif self.dia == Dia.miercoles:
            dia_cron = "WED"
        elif self.dia == Dia.jueves:
            dia_cron = "THU"
        elif self.dia == Dia.viernes:
            dia_cron = "FRI"
        elif self.dia == Dia.sabado:
            dia_cron = "SAT"
        else:
            dia_cron = "SUN"

        hora_cron = self.horario.split(":")[0]
        minutos_cron = self.horario.split(":")[1]

        return f"{minutos_cron} {hora_cron} * * {dia_cron}"