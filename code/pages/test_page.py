from flask import Flask, render_template, jsonify, session
from datetime import datetime
from decos import route

from pages._card_ import *

datos_usuarios = [
        {
            "_id": {
                "$oid": "676e4747ebe338def7159fb3"
            },
            "curp": "RACW050729MMCSHNA2",
            "nombre": "Wendy Lizeth",
            "apellido1": "Rascón",
            "apellido2": "Chávez",
            "estado_republica": "Estado de México",
            "delegacion_municipio": "Tlanepantla",
            "colonia": "Estado de México",
            "direccion": "La casa de Cosmo",
            "num_exterior": "55A",
            "num_interior": "5B",
            "codigo_postal": "14658",
            "fecha_nacimiento": "2005-07-29",
            "genero": "femenino",
            "nacionalidad": "mexicano",
            "playera": "c",
            "pantalon": "m",
            "calzado": "23.5",
            "banco": "Banco Bineo",
            "cuenta_bancaria": "5561468845135",
            "clabe": "",
            "email": "wendyl55@gmail.com",
            "telefono_fijo": "5555667788",
            "telefono_movil": "",
            "nivel_educativo": "medio superior",
            "situacion_educativa": "concluida",
            "lengua": "false"
        },
        {
            "_id": {
                "$oid": "676e52789f9fc2b163f4bd85"
            },
            "curp": "QKOR461085WFHRAYTU",
            "nombre": "Waneta",
            "apellido1": "Klugel",
            "apellido2": "Rosser",
            "estado_republica": "Aguascalientes",
            "delegacion_municipio": "Estribeiro",
            "colonia": "Lugovoy",
            "direccion": "163 Blue Bill Park Court",
            "num_exterior": "0404",
            "num_interior": "50117",
            "codigo_postal": "2580-444",
            "fecha_nacimiento": "1982-08-05",
            "genero": "Female",
            "nacionalidad": "mexicano",
            "playera": "S",
            "pantalon": "3XL",
            "calzado": 24.8,
            "banco": "CBM Banco",
            "cuenta_bancaria":"7337893086438",
            "email": "wrosser0@xing.com",
            "telefono_fijo": "3182926894",
            "telefono_movil": "3764452239",
            "nivel_educativo": "medio superior",
            "situacion_educativa": "concluida",
            "lengua": 'false',
            "estado": "rechazada",
        }
    ]

evaluaciones_ec1 = [
    {"claridad":"B", "comprension_lectora":"MB", "comprension_contenidos":"B", "eficiencia":"B", "trabajo_equipo":"MB", "asistencia":"MB", "observaciones":"Gran persona, con buena capacidad de dar clases, explica muy bien.", "tipoEvaluacion":"instructores", "fecha":"2021-10-10", "evento":"Evento 1"},
    {"claridad":"D", "comprension_lectora":"D", "comprension_contenidos":"B", "eficiencia":"B", "trabajo_equipo":"B", "asistencia":"MB", "observaciones":"Se esfuerza, pero le cuesta entender las cosas correctamente", "tipoEvaluacion":"instructores", "fecha":"2021-10-10", "evento":"Evento 2"},
]

evaluaciones_ec2 = [
    {"asistencia":"A", "relacion_comunidad":"A", "actitud":"A", "observaciones":"Da clases muy bien", "tipoEvaluacion":"instructores", "fecha":"2021-10-10"},
    {"asistencia":"A", "relacion_comunidad":"I", "actitud":"I", "observaciones":"Nunca falta, pero ha insultado a los padres de familia", "tipoEvaluacion":"instructores", "fecha":"2021-10-10"},
]

@route('/test')
def test_page():
    """Renderiza la página principal"""
    return render_template(f'test.html')

@route('/check_my_level')
def level_page():
    """Imprime el nivel que tiene guardado en session"""
    return render_template(f'test.html', echo=session['nivel'])

@route('/convenio_entrega')
def test1():
    datos_convocatoria = mapear_datos_convocatoria(datos_usuarios)

    cards = []
    for datos in datos_convocatoria:
        # Obtener las evaluaciones de la convocatoria
        evaluaciones = evaluaciones_ec1

        # Crear la carta
        card = Card.card_from_dict(EVALUACION_TEMPLATE, **datos)
        eval_cards = [
            Card.card_from_dict(EVALUACION_EC1_SECCION, **evaluacion)
            for evaluacion in evaluaciones
        ]
        card.extend(eval_cards)

        # Agregar la carta a la lista
        cards.append(card)
    
    return render_template('cartas.html', cards=cards, tipo_carta='carta_convenio')

@route('/datos_ec')
def test2():
    datos_convocatoria = mapear_datos_convocatoria(datos_usuarios)

    cards = []
    for datos in datos_convocatoria:
        # Obtener las evaluaciones de la convocatoria
        evaluaciones = evaluaciones_ec2

        # Crear la carta
        card = Card.card_from_dict(EVALUACION_TEMPLATE, **datos)
        eval_cards = [
            Card.card_from_dict(EVALUACION_EC2_SECCION, **evaluacion)
            for evaluacion in evaluaciones
        ]
        card.extend(eval_cards)

        # Agregar la carta a la lista
        cards.append(card)
    
    return render_template('cartas.html', cards=cards, tipo_carta='carta')