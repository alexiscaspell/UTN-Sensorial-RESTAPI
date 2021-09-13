from bson import ObjectId
from typing import Dict, Iterable
import pymongo
from mongoengine import (Document, DateTimeField, ComplexDateTimeField,
                         EmbeddedDocument, StringField, IntField, BooleanField,
                         ListField, DictField, EmbeddedDocumentField,
                         DecimalField, FloatField, ObjectIdField, DateTimeField
                         )

from apps.utils.logger_util import get_logger

logger = get_logger(__name__)


class EasyDocument:
    '''Esta clase es para facilitar los metodos feos que tiene mongoengine para
     manejar las actualizaciones de datos
    '''

    @classmethod
    def easy_update_one(cls, id: str, document) -> bool:
        '''Actualiza un documento de mongoengine a partir de su _id y un dict
        con los campos como las claves del diccionario y los valores se
        guardaran en la base'''

        dict_document = document

        if not isinstance(dict_document,dict):
            dict_document=mongo_to_dict(document,["_id"])
            
        return bool(cls.objects(id=ObjectId(id)).update_one(**dict(dict_document)))
        # prueba_dioct = dict(document)

        # return bool(cls.objects(id=ObjectId(id)).update_one(prueba_mongo))

    @classmethod
    def easy_delete_by_id(cls, id: str):
        '''Elimina un documento de mongo en base a su id'''
        return cls.objects(id=ObjectId(id)).delete()

    @classmethod
    def easy_get_documents(cls, skip: int = 0, limit: int = 50, filters: Dict = {}, exclude_fields=[],slice_fields=None,sort=None) -> Iterable[Dict]:
        '''Devuelve objetos de mongo'''

        skip = skip if skip else 0
        limit = limit if limit else 50
        filters = filters if filters else {}


        try:
            default_query = cls.objects(__raw__=filters)
            mongo_query = default_query[skip:skip+limit]
            
            # mongo_query = cls.objects(__raw__=filters)[skip:skip+limit]

            if slice_fields is not None:
                slice_fields_parameter = {f"slice__{k}":slice_fields[k] for k in slice_fields}

                mongo_query = default_query.fields(**slice_fields_parameter)[skip:skip+limit]

            if sort is not None:
                params=[k if sort[k]=="asc" else "-"+k for k in sort]
                mongo_query = mongo_query.order_by(*params)
                # mongo_query = mongo_query.sort([(k,pymongo.ASCENDING if v=="asc" else pymongo.DESCENDING) for k,v in sort])

            for elem in mongo_query:
                yield mongo_to_dict(elem, exclude_fields)

        except Exception as e:
            logger.error(e)
            for e in []:
                yield e

def mongo_to_dict(obj, exclude_fields=[]):
    return_data = []

    if obj is None:
        return None

    if isinstance(obj, Document):
        if "_id" not in exclude_fields:
            return_data.append(("_id", str(obj.id)))

        if "id" not in exclude_fields:
            return_data.append(("id", str(obj.id)))

    for field_name in obj._fields:

        if field_name in exclude_fields:
            continue

        # if field_name in ("id",):
        #     continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, list_field_to_dict(data)))
        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data, [])))
        elif isinstance(obj._fields[field_name], DictField):
            return_data.append((field_name, data))
        else:
            return_data.append(
                (field_name, mongo_to_python_type(obj._fields[field_name], data)))

    return dict(return_data)


def list_field_to_dict(list_field):

    return_data = []

    for item in list_field:
        if isinstance(item, EmbeddedDocument):
            return_data.append(mongo_to_dict(item, []))
        else:
            return_data.append(mongo_to_python_type(item, item))

    return return_data


def mongo_to_python_type(field, data):

    if data is None:
        return None

    if isinstance(field, DateTimeField):
        return field.to_python(data).isoformat()
    elif isinstance(field, (ComplexDateTimeField, DateTimeField)):
        return field.to_python(data).isoformat()
    elif isinstance(field, DictField):
        return dict(data)
    elif isinstance(field, StringField):
        return str(data)
    elif isinstance(field, FloatField):
        return float(data)
    elif isinstance(field, IntField):
        return int(data)
    elif isinstance(field, BooleanField):
        return bool(data)
    elif isinstance(field, ObjectIdField):
        return str(data)
    elif isinstance(field, DecimalField):
        return data
    else:
        return str(data)
