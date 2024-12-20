from typing import Literal

from mongo_objects._common_types_ import Nivel_acceso

class Credenciales:
    def __init__(
        self,
        usuario: str,
        contraseña: str,
        nivel: Nivel_acceso,
        **kwargs
    ):
        self.usuario = usuario
        self.contraseña = contraseña
        self.nivel = nivel