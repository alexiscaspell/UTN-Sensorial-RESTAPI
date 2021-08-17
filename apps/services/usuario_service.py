from apps.models.usuario import Usuario
from typing import Dict, List
from apps.repositories import usuario_repository


def get_all_usuarios() -> List[Usuario]:
    return usuario_repository.get_all_usuarios()
