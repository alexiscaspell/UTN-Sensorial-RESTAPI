from apps.models.indicador import Indicador
from mongoengine import (DateTimeField, Document, EmbeddedDocument, DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.models.usuario import Usuario
from apps.utils.mongo.odm import EasyDocument


class IndicadorDocument(Document, EasyDocument):
    name = StringField(required=True)
    sensors = ListField(required=True)
    limitSuperior = StringField(required=True)
    limitInferior = ListField(required=False)
    type = StringField(required=True)

    @staticmethod
    def from_model(model: Indicador):
        document = IndicadorDocument(**model.to_dict())
        return document
