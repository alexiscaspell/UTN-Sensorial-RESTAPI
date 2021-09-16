from apps.models.indicador import Indicador
from apps.models.sensor import Sensor
from mongoengine import (DateTimeField, Document, EmbeddedDocument, DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.utils.mongo.odm import EasyDocument

class SensorDocument(EmbeddedDocument, EasyDocument):
    id = ObjectIdField(db_field="_id",required=True)
    nombre = StringField(required=True)
    tipo = StringField(required=True)
    MAC = StringField(required=False)

    @staticmethod
    def from_model(model: Sensor):
        document = SensorDocument(**model.to_dict())
        return document


class IndicadorDocument(EmbeddedDocument, EasyDocument):
    meta = {"strict":False}
    
    id = ObjectIdField(db_field="_id",required=True)
    nombre = StringField(db_field="name",required=True)
    sensores = EmbeddedDocumentListField(SensorDocument,db_field="sensors",required=True)
    limite_superior = StringField(db_field="limitSuperior",required=True)
    limite_inferior = StringField(db_field="limitInferior",required=False)
    tipo = StringField(db_field="type",required=True)

    @staticmethod
    def from_model(model: Indicador):
        document = IndicadorDocument(**model.to_dict())
        return document
