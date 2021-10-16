from logging import INFO, ERROR, WARNING, DEBUG
import sys
import os


def is_environment_param():
    return len(sys.argv) > 1 and str(sys.argv) in ["development", "production"]


APP_NAME = "sensorial_restapi"
ENVIRONMENT_MODE = str(str(sys.argv[1]) if is_environment_param() else os.environ.get(
    f"{APP_NAME}".upper()+"_ENVIRONMENT_MODE", "development")).upper()

NO_MOSTRAR = ["DEBUG_MODE", "LOG_LEVEL", "DIRECTORIO_LOGS", "MONGODB_URL"]

DEVELOPMENT = {
    "DEBUG_MODE": True,
    "PYTHON_HOST": "0.0.0.0",
    "PYTHON_PORT":  5000,
    "API_BASE_PATH": "/api",
    "LOG_LEVEL": DEBUG,
    "DIRECTORIO_LOGS": "logs/",
    "DIRECTORIO_FILES": "files/",
    "AUTOCREAR_SENSORES": False,
    "MONGODB_URL": "mongodb+srv://prueba:prueba@localhost:27017/sensorial-db",
    "EMAIL_ENVIADOR": "un_email@gmail.com",
    "SMTP_USER": "un_email@gmail.com",
    "SMTP_PASS": "unapass",
    "SMTP_TLS": True,
    "SMTP_LOGIN": True,
    "SMTP_HOST": 'smtp.gmail.com',
    "SMTP_PORT": 587,
    "ENV": ENVIRONMENT_MODE
}
PRODUCTION = {
    "DEBUG_MODE": False,
    "PYTHON_HOST": "0.0.0.0",
    "PYTHON_PORT":  5000,
    "API_BASE_PATH": "/api",
    "LOG_LEVEL": INFO,
    "AUTOCREAR_SENSORES": False,
    "DIRECTORIO_LOGS": "logs/",
    "DIRECTORIO_FILES": "files/",
    "MONGODB_URL": "mongodb+srv://prueba:prueba@localhost:27017/sensorial-db",
    "EMAIL_ENVIADOR": "un_email@gmail.com",
    "SMTP_USER": "un_email@gmail.com",
    "SMTP_PASS": "unapass",
    "SMTP_TLS": True,
    "SMTP_LOGIN": True,
    "SMTP_HOST": 'smtp.gmail.com',
    "SMTP_PORT": 587,
    "ENV": ENVIRONMENT_MODE
}