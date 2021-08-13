from mongoengine import (DateTimeField, Document, EmbeddedDocument, DictField,
                         EmbeddedDocumentField, EmbeddedDocumentListField,
                         ListField, StringField, ObjectIdField)

from apps.models.objetivo import Objetivo
from apps.utils.mongo.odm import EasyDocument


class ObjetivoDocument(Document, EasyDocument):
    name = StringField(required=True)
    description = StringField(required=False)
    value = StringField(required=False)
    startDate = DateTimeField(required=False)
    endDate = DateTimeField(required=False)

    indicatorName = StringField(required=False)
    indicatorId = StringField(required=False)

    @staticmethod
    def from_model(model: Objetivo):
        document = ObjetivoDocument(**model.to_dict())
        return document
