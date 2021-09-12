from apps.models.indicador import Indicador
from apps.models.medicion import Medicion
from apps.utils.mongo.odm import EasyDocument
from mongoengine import (DateTimeField, DictField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         FloatField, ListField, ObjectIdField, StringField)


class MedicionDocument(Document, EasyDocument):
    meta = {'collection': 'samples'}

    valor = FloatField(required=True)
    unidad = StringField(required=False)
    MAC = StringField(required=True)
    tipo_sensor = StringField(required=True)
    fecha = DateTimeField(required=True)

    @staticmethod
    def from_model(model: Medicion):
        document = MedicionDocument(**model.to_dict())
        return document
