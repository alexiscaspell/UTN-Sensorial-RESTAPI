import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Tuple

from apps.models.email import Email

_SMT_HOST = 'smtp.gmail.com'
_SMT_PORT = 587
# _SMT_PORT = 465


def enviar_email(email_a_enviar: Email):
    '''
    Envia el email
    '''
    server = smtplib.SMTP(_SMT_HOST,_SMT_PORT)
    
    server.ehlo()
    server.starttls()
    server.ehlo()
    
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


def _preparar_adjuntos(adjuntos: List[Tuple[str, bytes]]) -> List[MIMEBase]:
    '''
    Prepara los adjuntos para el enviador de emails
    '''
    resultado = []
    for adjunto in adjuntos:

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
