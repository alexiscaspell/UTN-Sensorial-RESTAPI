from apps.models.indicador import Indicador
from apps.utils.mongo.mongo_connector import MongoQueryBuilder
from apps.repositories.entities.usuario_entity import UsuarioDocument
from apps.utils.mongo import mongo_connector
from apps.models.exception import UsuarioNotFoundException
from apps.models.usuario import Usuario
from typing import List,Dict

def get_por_id(id) -> Indicador:
    indicador_dict = mongo_connector.get_by_id(IndicadorDocument,id)

    if indicador_dict is None:
        return None

    return Indicador(indicador_dict)