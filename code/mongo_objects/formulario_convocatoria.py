from typing import Literal, Optional, Union

Talla = Literal['Chico', 'Mediano', 'Grande', 'Extra Grande']
Genero = Literal['masculino', 'femenino', 'otro']
Nacionalidad = Literal['mexicano', 'extranjero']
Situacion_educativa = Literal['concluida', 'cursando', 'trunca']
Nivel_educativo = Literal['primaria', 'secundaria', 'medio superior', 'superior']
Estado_convocatoria = Optional[Literal['aceptada', 'rechazada']]
Booleano_textual = Union[Literal['true', 'false'], bool]

class FormularioConvocatoria:
    def __init__(
        self,
        curp: str,
        nombre: str,
        apellido1: str,
        estado_republica: str,
        delegacion_municipio: str,
        colonia: str,
        direccion: str,
        num_exterior: str,
        codigo_postal: str,
        fecha_nacimiento: str,
        genero: Genero,
        nacionalidad: Nacionalidad,
        playera: Talla,
        pantalon: Talla,
        calzado: float,
        banco: str,
        cuenta_bancaria: str,
        lengua: Booleano_textual,
        situacion_educativa: Situacion_educativa,
        nivel_educativo: Nivel_educativo,
        año_convocatoria: str,

        apellido2: Optional[str] = None,
        num_interior: Optional[str] = None,
        estado: Estado_convocatoria = None,
        clabe: Optional[str] = None,
        email: Optional[str] = None,
        telefono_fijo: Optional[str] = None,
        telefono_movil: Optional[str] = None,
        **kwargs
    ):

        # Inicializar los datos
        self.curp = curp
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.estado_republica = estado_republica
        self.delegacion_municipio = delegacion_municipio
        self.colonia = colonia
        self.direccion = direccion
        self.num_exterior = num_exterior
        self.num_interior = num_interior
        self.codigo_postal = codigo_postal
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.nacionalidad = nacionalidad
        self.playera = playera
        self.pantalon = pantalon
        self.calzado = calzado
        self.banco = banco
        self.cuenta_bancaria = cuenta_bancaria
        self.clabe = clabe
        self.lengua = lengua if type(lengua) == bool else lengua == 'true'
        self.email = email
        self.telefono_fijo = telefono_fijo
        self.telefono_movil = telefono_movil
        self.situacion_educativa = situacion_educativa
        self.nivel_educativo = nivel_educativo
        self.estado = estado
        self.año_convocatoria = año_convocatoria
        
if __name__ == '__main__':
    example = {
        "_id": {
            "$oid": "673fc8bb8813af7022b16933"
        },
        "curp": "HELI031122HHGRCBA8",
        "nombre": "Ibrahin Abraham",
        "apellido1": "Hernández",
        "apellido2": "Lucio",
        "direccion": "Lázaro Cárdenas",
        "num_exterior": "2",
        "num_interior": "1",
        "codigo_postal": "07710",
        "fecha_nacimiento": "2003-11-22",
        "genero": "masculino",
        "nacionalidad": "mexicano",
        "playera": "m",
        "pantalon": "m",
        "lengua": False,
        "calzado": "27",
        "banco": "BBVA México",
        "cuenta_bancaria": "1234567890",
        "clabe": "",
        "email": "aloibra49@gmail.com",
        "telefono_fijo": "",
        "telefono_movil": "7261261182",
        "nivel_educativo": "superior",
        "situacion_educativa": "cursando",
        "estado": "rechazada",
        "año_convocatoria": "2024"
    }

    formulario = FormularioConvocatoria(**example)
    print(formulario)
    print(vars(formulario))
    print(f'La curp de {formulario.nombre} {formulario.apellido1} {formulario.apellido2 or '\b'} es {formulario.curp}')
