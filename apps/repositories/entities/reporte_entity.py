from apps.models.reporte import Reporte
from apps.utils.mongo.odm import EasyDocument
from mongoengine import (EmbeddedDocument, ListField,
                         ObjectIdField, StringField)


class ReporteDocument(EmbeddedDocument, EasyDocument):
    id = ObjectIdField(db_field="_id", required=False)
    destinatarios = ListField(required=True)
    nombre = StringField(required=True)
    descripcion = StringField(required=False)
    dia = StringField(required=True)
    horario = StringField(required=True)

    @staticmethod
    def from_model(model: Reporte):
        document = ReporteDocument(**model.to_dict())
        return document
