'''Este loader actualiza una coleccion de mongo leyendo registro por registro
de la general table'''

from typing import TYPE_CHECKING, Dict, List

from apps.utils.logger_util import get_logger
from bson import ObjectId
from mongoengine import (BooleanField, DateTimeField, DictField, Document,
                         StringField, connect)
from mongoengine.errors import NotUniqueError, ValidationError
from apps.utils.mongo.odm import EasyDocument

logger = get_logger("MongoConnector")

# CONEXION A LA BD
# connect(host=CurrentConfig.MONGODB)


class MongoQuery:
    def __init__(self, collection: EasyDocument, mongo_query_spec: Dict):
        self.collection = collection
        self.filters = mongo_query_spec.get("filters", None)
        self.page_number = mongo_query_spec.get("page_number", None)
        self.items_per_page = mongo_query_spec.get("items_per_page", None)
        self.exclude_fields = mongo_query_spec.get("exclude_fields", [])
        self.slice_fields = mongo_query_spec.get("slice_fields", None)
        self.sort = mongo_query_spec.get("sort", None)
        self.returned_fields = mongo_query_spec.get("returned_fields", None)


class MongoQueryBuilder:
    def __init__(self, collection: EasyDocument):
        self.mongo_query = MongoQuery(collection, {})

    def filters(self, filters):
        self.mongo_query.filters = filters
        return self

    def add_id_filter(self, value):
        return self.add_filter({"_id":ObjectId(value)})
        
    def add_filter(self, filter):
        if self.mongo_query.filters is None:
            self.mongo_query.filters = {}
        self.mongo_query.filters.update(filter)
        return self

    def page(self, page_number, page_size):
        self.mongo_query.page_number = page_number
        self.mongo_query.items_per_page = page_size
        return self

    def exclude_fields(self, exclude_fields):
        self.mongo_query.exclude_fields = exclude_fields
        return self

    def add_exclude_field(self, exclude_field):
        self.mongo_query.exclude_fields.append(exclude_field)
        return self

    def add_slice_field(self, slice_field, page_number, page_size):
        if self.mongo_query.slice_fields is None:
            self.mongo_query.slice_fields = {}
        self.mongo_query.slice_fields.update(
            {slice_field: [page_number*page_size, page_size]})
        return self

    def sort_by(self,sort_spec:dict):
        if self.mongo_query.sort is None:
            self.mongo_query.sort = {}
            
        self.mongo_query.sort.update(sort_spec)

        return self

    def add_return_field(self,return_field:dict):
        if self.mongo_query.returned_fields is None:
            self.mongo_query.returned_fields = {}
            
        self.mongo_query.returned_fields.update(return_field)

        return self

    def build(self):
        return self.mongo_query


def insert(some_document):
    return some_document.save().id


def update(some_document, dict_document: Dict = None):

    if not dict_document:
        dict_document = some_document

    some_document.easy_update_one(some_document.id, dict_document)


def get_by_filter(query: MongoQuery) -> List[Dict]:

    offset = (query.page_number - 1) * \
        query.items_per_page if query.page_number and query.items_per_page else 0

    elems = []

    for o in query.collection.easy_get_documents(skip=offset, limit=query.items_per_page, filters=query.filters, exclude_fields=query.exclude_fields, slice_fields=query.slice_fields,sort=query.sort):
        elems.append(o)

    return elems


def get_by_id(document_class: Document, id: str) -> Dict:
    '''Retorna un diccionario con el documento perteneciente a id'''

    builder = MongoQueryBuilder(document_class).add_filter(
        {"_id": ObjectId(id)}).page(0, 1).add_exclude_field("_id")

    list_result = get_by_filter(builder.build())

    if list_result == [] or list_result is None:
        return None

    return list_result[0]


def get_by_ids(document_class: Document, ids_list: List[str]) -> List[Dict]:
    '''Retorna una lista de diccionarios con los documentos pertenecientes a la lista de ids'''

    builder = MongoQueryBuilder(document_class).add_filter({
        "id": {"$in": ids_list}})

    list_result = get_by_filter(builder.build())

    return list_result

# connect(
#     username=CurrentConfig.MONGODB_USER,
#     password=CurrentConfig.MONGODB_PASS,
#     host=CurrentConfig.MONGODB,
#     authentication_source='admin'
# )
