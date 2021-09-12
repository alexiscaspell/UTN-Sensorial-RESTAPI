from apps.models.indicador import Indicador
from mongoengine import (DateTimeField, Document, EmbeddedDocument, DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.models.usuario import Usuario
from apps.utils.mongo.odm import EasyDocument


class IndicadorDocument(EmbeddedDocument, EasyDocument):
    id = ObjectIdField(db_field="_id",required=True)
    nombre = StringField(db_field="name",required=True)
    sensores = ListField(db_field="sensors",required=True)
    limite_superior = StringField(db_field="limitSuperior",required=True)
    limite_inferior = StringField(db_field="limitInferior",required=False)
    tipo = StringField(db_field="type",required=True)

    @staticmethod
    def from_model(model: Indicador):
        document = IndicadorDocument(**model.to_dict())
        return document
