from typing import List
from flask import render_template, request, redirect, url_for, session, jsonify, make_response, Response
from decos import route, nav
import requests

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._card_ import *
from pages._error_ import ConafeException

CAPTACION_URL = get_url('captacion')
CAPACITACION_URL = get_url('capacitacion')

@route('/educadores')
@nav('Educadores')
@restricted('ECA')
def educadores():
    """Renderiza el panel de control y las convocatorias."""
    # Obtener los datos del microservicio
    try:
        response = requests.post(CAPTACION_URL + '/get_capacitacion', json={'estado': session['estado']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
        
    educadores: List = microservice_data["result"]

    try:
        response = requests.post(CAPTACION_URL + '/get_educadores', json={'estado': session['estado']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

    educadores.extend(microservice_data["result"])
    educadores = mapear_datos_convocatoria(educadores)

    cards = []
    for educador in educadores:
        folio = educador["folio"]

        try:
            response = requests.post(CAPACITACION_URL + '/get_evaluaciones', json={'folio':folio})
            response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
            microservice_data = response.json()  # Obtiene el JSON del microservicio
        except requests.RequestException as e:
            raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
        
        evaluaciones = microservice_data["result"]
        card = Card.card_from_dict(EVALUACION_TEMPLATE, **educador)

        eval_cards = []
        for evaluacion in evaluaciones:
            template = EVALUACION_EC1_SECCION if evaluacion['tipo'] == 'ec1' \
                else EVALUACION_EC2_SECCION
            
            carta = Card.card_from_dict(template, **evaluacion)
            eval_cards.append(carta)

        card.extend(eval_cards)
        cards.append(card)

    return render_template('cartas.html', cards=cards, tipo_carta='carta', stylesheets=['button'])
