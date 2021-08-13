from apps.models.indicador import Indicador
from apps.models.usuario import Usuario
from apps.repositories.entities.indicador_entity import IndicadorDocument
from apps.repositories.entities.objetivo_entity import ObjetivoDocument
from apps.repositories.entities.reporte_entity import ReporteDocument
from apps.utils.mongo.odm import EasyDocument
from mongoengine import (DateTimeField, DictField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, ObjectIdField, StringField)


class IndicadorDocument(Document, EasyDocument):
    meta = {'collection': 'dashboards'}

    sensors = ListField(required=True)
    limitSuperior = StringField(required=True)
    limitInferior = ListField(required=False)

    descripcion = StringField(required=False)
    nombre = StringField(required=True)
    fecha_creacion = DateTimeField(required=False)

    reportes = EmbeddedDocumentListField(ReporteDocument)
    objetivos = EmbeddedDocumentListField(ObjetivoDocument)
    indicadores = EmbeddedDocumentListField(IndicadorDocument)

    @staticmethod
    def from_model(model: Indicador):
        document = IndicadorDocument(**model.to_dict())
        return document


