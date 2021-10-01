import apps.configs.configuration as conf
from apps.configs.vars import Vars
from apps.utils.logger_util import get_logger
from apps.models.email import Email,MailTemplate
from apps.models.receptor_estado import ReceptorDeEstado
import apps.utils.email_util as email_util


logger = get_logger(__name__)

_EMAIL_ENVIADOR = conf.get(Vars.EMAIL_ENVIADOR)
_EMAIL_PASS = conf.get(Vars.EMAIL_PASS)

def enviar_mail(receptor_estado:ReceptorDeEstado):
    '''
    Envia un mail con el status de la tarea a los receptores
    '''
    encabezado = receptor_estado.template.encabezado
    cuerpo = receptor_estado.template.cuerpo

    destinatarios = receptor_estado.destinatarios
    copiados = receptor_estado.en_copia

    adjuntos = receptor_estado.template.adjuntos

    cuerpo_html = receptor_estado.template.cuerpo_html

    email_a_enviar = Email.from_dict( {"de" : _EMAIL_ENVIADOR,
                            "contrasenia" : _EMAIL_PASS,
                            "para" : destinatarios,
                            "encabezado" : encabezado,
                            "cuerpo" : cuerpo,
                            "copia" : copiados,
                            "adjuntos":adjuntos,"cuerpo_html":cuerpo_html})

    email_util.enviar_email(email_a_enviar)