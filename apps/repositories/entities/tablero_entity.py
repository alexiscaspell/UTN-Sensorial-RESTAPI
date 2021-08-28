from apps.models.sensor import Sensor
from apps.models.tablero import Tablero
from apps.repositories.entities.indicador_entity import IndicadorDocument
from apps.repositories.entities.objetivo_entity import ObjetivoDocument
from apps.repositories.entities.reporte_entity import ReporteDocument
from apps.utils.mongo.odm import EasyDocument
from mongoengine import (DateTimeField, DictField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, ObjectIdField, StringField)


class SensorTableroDocument(EmbeddedDocument, EasyDocument):

    nombre = StringField(required=True)
    tipo = StringField(required=True)

    @staticmethod
    def from_model(model: Sensor):
        document = SensorTableroDocument(**model.to_dict())
        return document
class TableroDocument(Document, EasyDocument):
    meta = {'collection': 'dashboards',"strict":False}

    nombre = StringField(required=True)
    descripcion = StringField(required=False)
    fecha_creacion = DateTimeField(required=False)

    reportes = EmbeddedDocumentListField(ReporteDocument)
    objetivos = EmbeddedDocumentListField(ObjetivoDocument)
    indicadores = EmbeddedDocumentListField(IndicadorDocument)

    @staticmethod
    def from_model(model: Tablero):
        document = TableroDocument(**model.to_dict())
        return document


