from typing import Literal

from mongo_objects._common_types_ import Estado_republica

Tipo_evaluacion = Literal['instructores','capacitadores','asistentes']
Evaluacion_capacidad = Literal['D', 'B', 'MB'] # Significan Deficiente, Bien y Muy Bien

class Evaluacion_EC1:
    def __init__(
        self,
        estado: Estado_republica,
        evento: str,
        fecha: str,
        tipo_evaluacion: Tipo_evaluacion,
        nombre: str,
        claridad: Evaluacion_capacidad,
        comprension_lectora: Evaluacion_capacidad,
        comprension_contenidos: Evaluacion_capacidad,
        eficiencia: Evaluacion_capacidad,
        trabajo_equipo: Evaluacion_capacidad,
        asistencia: Evaluacion_capacidad,
        observaciones: str,
        **kwargs
    ):
        self.estado = estado
        self.evento = evento
        self.fecha = fecha
        self.tipo_evaluacion = tipo_evaluacion
        self.nombre = nombre
        self.claridad = claridad
        self.comprension_lectora = comprension_lectora
        self.comprension_contenidos = comprension_contenidos
        self.eficiencia = eficiencia
        self.trabajo_equipo = trabajo_equipo
        self.asistencia = asistencia
        self.observaciones = observaciones

Evaluacion_adecuada = Literal['A', 'I'] # Significan Adecuada e Inadecuada

class Evaluacion_EC2:
    def __init__(
        self,
        estado: Estado_republica,
        evento: str,
        fecha: str,
        tipo_evaluacion: Tipo_evaluacion,
        nombre: str,
        asistencia: Evaluacion_adecuada,
        relacion_comunidad: Evaluacion_adecuada,
        actitud: Evaluacion_adecuada,
        observaciones: str,
        **kwargs
    ):
        self.estado = estado
        self.evento = evento
        self.fecha = fecha
        self.tipo_evaluacion = tipo_evaluacion
        self.nombre = nombre
        self.asistencia = asistencia
        self.relacion_comunidad = relacion_comunidad
        self.actitud = actitud
        self.observaciones = observaciones