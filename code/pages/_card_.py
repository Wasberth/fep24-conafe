import re
from typing import List, Dict

CONVOCATORIA_TEMPLATE = '{nombre} {apellido}#Datos personales:{curp}|CURP;{fecha_nacimiento}|Fecha de Nacimiento>{genero}|Género;{nacionalidad}>>{lengua}|Habla lengua indígena>>{nivel_educativo} ({situacion_educativa})|Nivel Educativo#Dirección:{estado_republica}|Estado>{delegacion_municipio}|Delegacion/Municipio>>{colonia};{codigo_postal}>{direccion}#Tallas:{playera}>{pantalon}>{calzado}#Cuenta de Banco:{banco}>{cuenta_bancaria}|Cuenta#Datos de Contacto:{email};{telefono_fijo};{telefono_movil}'

class Field:
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

class Column:
    def __init__(self, fields: List[Field]):
        self.fields = fields

    def __iter__(self):
        return iter(self.fields)

class Row:
    def __init__(self, columns: List[Column]):
        self.columns = columns

    def __iter__(self):
        return iter(self.columns)

class Section:
    def __init__(self, title: str, rows: List[Row]):
        self.title = title
        self.content = rows

class Card:
    def __init__(self, title: str, sections: List[Section], raw_data: Dict[str, any] = None):
        self.title = title
        self.content = sections
        self.raw = raw_data

    @staticmethod
    def card_from_dict(template: str, *args, **kwargs):
        """
        Crea una carta a partir de un diccionario y un template
        :param str template: Template de la carta
            Los campos a reemplazar deben estar entre llaves
            El formato para la plantilla es el siguiente:
            título#seccion1:campo1;campo2|Alias>campo3;campo4>>campo5>campo6#seccion2:campo7;campo8>campo9
            # representa un cambio de sección, el texto antes de : es su título
            >> representa un salto de fila
            > representa un salto de columna
            ; separa campos
            | representa que el campo tiene un alias, el texto después de | es el alias
        :param dict args: Diccionario con los valores a reemplazar
        """

        def replace_placeholders(text: str, field_data: Dict[str, any]) -> str:
            """Reemplaza los placeholders en el texto usando el diccionario de datos."""
            def replacer(match):
                key = match.group(1)
                data = field_data.get(key)

                if data is None:
                    return 'No proporcionado'

                if type(data) == bool:
                    return 'Sí' if data else 'No'
                
                if data == 'false':
                    return 'No'
                
                if data == 'true':
                    return 'Sí'
                
                if data == '':
                    return 'No proporcionado'

                return str(data)
            
            return re.sub(r'\{(.*?)\}', replacer, text)

        # Merge args and kwargs into a single dictionary
        field_data = {}
        if len(args) == 1 and isinstance(args[0], dict):
            field_data.update(args[0])
        field_data.update(kwargs)

        # Parse the template string
        parts = template.split('#')
        title = replace_placeholders(parts[0], field_data)
        sections = []

        for section_part in parts[1:]:
            section_title, section_body = section_part.split(':', 1)
            section_title = replace_placeholders(section_title, field_data)

            rows = []
            for row in section_body.split('>>'):
                cols = []
                for col in row.split('>'):
                    fields = []
                    for field in col.split(';'):
                        print(field)
                        if '|' in field:
                            value, label = field.split('|', 1)
                        else:
                            value, label = field, field
                            label = label.replace('_', ' ')
                            label = re.sub(r'\{(.*?)\}', r'\1', label).title()
                            

                        value = replace_placeholders(value, field_data)
                        label = replace_placeholders(label, field_data)
                        fields.append(Field(label, value))
                    cols.append(Column(fields))
                rows.append(Row(cols))
            sections.append(Section(section_title, rows))

        return Card(title, sections, field_data)
    
