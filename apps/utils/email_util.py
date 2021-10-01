import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Tuple
import os
from apps.models.email import Email, Adjunto
from apps.utils.logger_util import get_logger

_SMT_TLS = True
_SMT_LOGIN = True
_SMT_HOST = 'smtp.gmail.com'
_SMT_PORT = 587
# _SMT_PORT = 465
logger = get_logger(__name__)


def enviar_email(email_a_enviar: Email):
    '''
    Envia el email
    '''
    server = smtplib.SMTP(_SMT_HOST, _SMT_PORT)

    if _SMT_TLS:
        logger.info("USANDO TLS ...")
        server.ehlo()
        server.starttls()
        server.ehlo()

    if _SMT_LOGIN:
        logger.info(f"LOGIN: {email_a_enviar.usuario}, {email_a_enviar.contrasenia} ...")
        server.login(email_a_enviar.usuario, email_a_enviar.contrasenia)

    destinatarios = email_a_enviar.para + email_a_enviar.copia
    text = _preparar_email(email_a_enviar)

    server.sendmail(email_a_enviar.de, destinatarios, text)


def _preparar_email(email_a_enviar: Email) -> str:
    '''
    Preparar email para el enviador de email
    '''
    message = MIMEMultipart()
    message["From"] = email_a_enviar.de
    message["To"] = ', '.join(email_a_enviar.para)
    message["Subject"] = email_a_enviar.encabezado
    message["Bcc"] = ', '.join(email_a_enviar.copia)

    message.attach(MIMEText(email_a_enviar.cuerpo, "plain"))

    if email_a_enviar.cuerpo_html:
        message.attach(MIMEText(email_a_enviar.cuerpo_html, "html"))

    for part in _preparar_adjuntos(email_a_enviar.adjuntos):
        message.attach(part)

    return message.as_string()


def _preparar_adjuntos(adjuntos: List[Adjunto]) -> List[MIMEBase]:
    '''
    Prepara los adjuntos para el enviador de emails
    '''

    resultado = []
    adjuntos_raw = [a.raw() for a in adjuntos]

    for adjunto in adjuntos_raw:

        nombre = adjunto[0]
        contenido = adjunto[1]

        part = MIMEBase("application", "octet-stream")
        part.set_payload(contenido)

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {nombre}",
        )

        resultado.append(part)

    return resultado
