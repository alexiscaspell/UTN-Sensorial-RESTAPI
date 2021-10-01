from mongoengine import (DateTimeField, Document, EmbeddedDocument, DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.models.objetivo import Objetivo
from apps.utils.mongo.odm import EasyDocument


class ObjetivoDocument(EmbeddedDocument, EasyDocument):
    id = ObjectIdField(db_field="_id",required=False)
    nombre = StringField(db_field="name",required=True)
    decripcion = StringField(db_field="description",required=False)
    valor = StringField(db_field="value",required=True)
    fecha_inicial = DateTimeField(db_field="startDate",required=False)
    fecha_final = DateTimeField(db_field="endDate",required=False)

    id_indicador = StringField(db_field="indicatorId",required=False)
    nombre_indicador = StringField(db_field="indicatorName",required=False)

    @staticmethod
    def from_model(model: Objetivo):
        document = ObjetivoDocument(**model.to_dict())
        return document
