from apps.utils.mongo.mongo_connector import MongoQueryBuilder
from apps.repositories.entities.usuario_entity import UsuarioDocument
from apps.utils.mongo import mongo_connector
from apps.models.exception import UsuarioNotFoundException
from apps.models.usuario import Usuario
from typing import List,Dict

def _get_usuarios():
    try:

        query = MongoQueryBuilder(UsuarioDocument).add_exclude_field("_id").build()
        resultados = mongo_connector.get_by_filter(query)

        if not resultados:
            raise UsuarioNotFoundException()

        usuarios=[]

        for u in resultados:
            usuario = Usuario(u)
            usuarios.append(usuario)

        return usuarios
    except Exception as e:
        pass

    return []

def get_all_usuarios() -> List[Usuario]:
    return _get_usuarios()