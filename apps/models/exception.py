from enum import Enum
from functools import wraps

from flask import jsonify

from apps.utils.logger_util import get_logger

HTTP_STATUS_ERROR_NEGOCIO = 409


class AppException(Exception):
    '''
    Clase de error basico para manejar errores de negocio o errores dentro de la aplicacion
    que son esperados sus atributos son:

    codigo: usado para quien quiera atrapar la excepcion, se puede usar un str de la forma 'ERROR_ALTA_USUARIO'
    o un codigo numerico, la idea es que alguien pueda hacer un if con este codigo pudiendo hacer algo al respecto

    mensaje: contiene informacion extra en formato texto para una mayor informacion, esto es mas para quien use la api,
    un ejemplo puede ser: 'el usuario ya existe en la base de datos'
    '''

    def __init__(self, codigo, mensaje):
        self.codigo = codigo.value if isinstance(codigo, Enum) else codigo
        self.mensaje = mensaje

    def to_dict(self):
        return {'codigo': self.codigo, 'mensaje': self.mensaje}

    def respuesta_json(self):
        return jsonify(self.to_dict()), HTTP_STATUS_ERROR_NEGOCIO

class UnauthoricedException(AppException):
    def __init__(self):
        super().__init__(401, 'Usuario no autorizado')

    def __str__(self):
        return self.mensaje


class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(400, 'Token invalido')

    def __str__(self):
        return self.mensaje
class UsuarioNotFoundException(AppException):
    def __init__(self):
        super().__init__(500, 'Usuario no encontrado.')

    def __str__(self):
        return self.mensaje
class DatabaseException(AppException):
    def __init__(self,mensaje="Error en base de datos."):
        super().__init__(500, mensaje)

    def __str__(self):
        return self.mensaje

class IndicadorNotFoundException(AppException):
    def __init__(self,id_indicador=None):
        super().__init__(409, f"Indicador con id {id_indicador} no encontrado.")

class TableroNotFoundException(AppException):
    def __init__(self,id_tablero=None):
        super().__init__(409, f"Tablero con id {id_tablero} no encontrado.")

    def __str__(self):
        return self.mensaje

class ObjetivoNotFoundException(AppException):
    def __init__(self,id_objetivo=None):
        super().__init__(409, f"Objetivo con id {id_objetivo} no encontrado.")

    def __str__(self):
        return self.mensaje
        
class ObjetivoInvalidoException(AppException):
    def __init__(self,id_objetivo=None):
        super().__init__(409, f"Objetivo con id {id_objetivo} invalido.")

    def __str__(self):
        return self.mensaje

class ReporteInvalidoException(AppException):
    def __init__(self,id_reporte=None):
        super().__init__(409, f"Reporte con id {id_reporte} invalido.")

    def __str__(self):
        return self.mensaje

class ReporteYaExistenteException(AppException):
    def __init__(self,nombre_reporte=None):
        super().__init__(409, f"Reporte con nombre {nombre_reporte} ya existente.")

    def __str__(self):
        return self.mensaje
