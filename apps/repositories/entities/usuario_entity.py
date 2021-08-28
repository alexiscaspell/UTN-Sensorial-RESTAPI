from mongoengine import (DateTimeField, Document, EmbeddedDocument,DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.models.usuario import Usuario
from apps.utils.mongo.odm import EasyDocument


class UsuarioDocument(Document, EasyDocument):
    meta = {'collection': 'usuarios'}

    password = StringField(required=True)
    rol = StringField(required=True)
    nombre = StringField(required=True)
    mail = StringField(required=True, max_length=256)
    fecha_creacion = DateTimeField(required=True)
    ultimo_login = DateTimeField(required=False)

    @staticmethod
    def from_model(model: Usuario):
        document = UsuarioDocument(**model.to_dict())
        return document