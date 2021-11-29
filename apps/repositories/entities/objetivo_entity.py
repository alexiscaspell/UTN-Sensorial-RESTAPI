from mongoengine import (DateTimeField, Document, EmbeddedDocument, DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.models.objetivo import Objetivo
from apps.utils.mongo.odm import EasyDocument


class ObjetivoDocument(EmbeddedDocument, EasyDocument):
    meta = {"strict":False}

    id = ObjectIdField(db_field="_id",required=False)
    nombre = StringField(db_field="name",required=True)
    descripcion = StringField(db_field="description",required=False)
    valor = StringField(db_field="value",required=True)
    valor_calculado = StringField(db_field="calculatedValue",required=False)
    fecha_inicial = StringField(db_field="startDate",required=False)
    fecha_final = StringField(db_field="endDate",required=False)

    id_indicador = StringField(db_field="indicatorId",required=True)
    nombre_indicador = StringField(db_field="indicatorName",required=False)

    @staticmethod
    def from_model(model: Objetivo):
        document = ObjetivoDocument(**model.to_dict())
        return document
