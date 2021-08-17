from apps.models.indicador import Indicador
from apps.models.sensor import Sensor
from apps.models.usuario import Usuario
from apps.utils.mongo.odm import EasyDocument
from mongoengine import (DateTimeField, DictField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, ObjectIdField, StringField)


class SensorDocument(Document, EasyDocument):
    meta = {'collection': 'sensores'}

    nombre = StringField(required=True)
    tipo = StringField(required=True)

    @staticmethod
    def from_model(model: Sensor):
        document = SensorDocument(**model.to_dict())
        return document
