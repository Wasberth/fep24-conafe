from typing import Literal, Optional, Union

from mongo_objects._common_types_ import Estado_republica

class CCT:
    def __init__(
        self,
        clave: str,
        nombre: str,
        estado: Estado_republica,
        municipio: str,
        comunidad: str,
        sede: Optional[str] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        self.clave = clave
        self.nombre = nombre
        self.estado = estado
        self.municipio = municipio
        self.comunidad = comunidad
        self.sede = sede
        self.region = region