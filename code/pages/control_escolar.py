from flask import render_template, request, jsonify, make_response
from decos import route, nav
import requests

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._decompose_form_ import decompose_form
from pages._error_ import ConafeException

CAPTACION_URL = get_url('captacion')

@route('/alumno/alta')
@nav('Control Escolar/Altas')
@restricted(['EC2', 'ECA'])
def alta_alumno():
    return render_template(
        f'alta_alumno.html',
        stylesheets=['button'],
        scripts=['addStudent']
    )

@route('/alta_alumno_bd', methods=['POST'])
def alta_alumno_bd():
    form_data = request.form.to_dict()
    form_data = {"registros":decompose_form(form_data)}

    try:
        response = requests.post(CAPTACION_URL + '/registrar_alumno', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", details=str(e))
    
    return make_response(render_template(f'success.html',
                stylesheets=['success', 'button'],
                title='Registro Concluido',
                extra_info=f'Los alumnos han sido dados de alta correctamente!'
            ))

"""
@route('/alumno/baja')
@nav('Control Escolar/Bajas y Reinscripciones')
@restricted(['EC2', 'ECA'])
def baja_alumno():
    return render_template(
        f'baja_alumno.html',
        stylesheets=['button'],
        scripts=['removeStudent']
    )
"""