from flask import render_template, request, session, make_response, url_for
from decos import route, nav, offline
import requests
from pages._card_ import *

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._decompose_form_ import decompose_form
from pages._error_ import ConafeException

CAPTACION_URL = get_url('captacion')
UBICACION_URL = get_url('ubicacion')

@route('/alumno/alta')
@nav('Control Escolar/Altas')
@offline()
@restricted(['EC2', 'ECA'])
def alta_alumno():
    datos = {}
    if estado := session.get('estado'):
        datos['estado'] = estado

    if sede := session.get('sede'):
        datos['cct'] = [{'nombre':sede, 'sede':sede}]
    else:
        try:
            response = requests.get(UBICACION_URL + '/lista_lugares', json={'estado':estado.upper()})
            response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
            microservice_data = response.json()  # Obtiene el JSON del microservicio
            datos['cct'] = microservice_data['result']
        except requests.RequestException as e:
            raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

    return render_template(
        f'alta_alumno.html',
        stylesheets=['button'],
        scripts=['addStudent'],
        **datos
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
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    return make_response(render_template(f'success.html',
                stylesheets=['success', 'button'],
                title='Registro Concluido',
                extra_info=f'Los alumnos han sido dados de alta correctamente!'
            ))

@route('/alumno/reinscripcion_busqueda')
@nav('Control Escolar/Reinscripción')
@restricted(['EC2', 'ECA'])
def reinscripcion_alumno_busqueda():
    """Renderiza la página donde se buscará el alumno dependiendo del curp"""
    return render_template(f'reinscribir_alumno_busqueda.html', stylesheets=['button'])

@route('/alumno/reinscripcion', methods=['POST'])
@restricted(['EC2', 'ECA'])
def reinscripcion_alumno():
    form_data = request.form.to_dict()

    query = {"estado": session["estado"], "curp": form_data["curp"]}
    try:
        response = requests.get(CAPTACION_URL + '/get_alumno_baja', json=query)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

    alumnos = microservice_data['result'] 
    try:
        cards = [Card.card_from_dict(ALUMNO_TEMPLATE, **alumno) for alumno in alumnos]
    except Exception as e:
        raise ConafeException(500,"No se encontró el CURP.")
    return render_template('cartas.html', cards=cards, tipo_carta='carta_reinscripcionalumno', stylesheets=['button'])

@route('/reinscripcion_alumno_bd/<curp>', methods=['POST'])
def reinscripcion_alumno_bd(curp):

    query = {'curp': curp}

    try:
        response = requests.post(CAPTACION_URL + '/reinscribir_alumno', json=query)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    return make_response(render_template(f'success.html',
                stylesheets=['success', 'button'],
                title='Alumno reinscrito correctamente!',
                redirect=url_for('reinscripcion_alumno_busqueda'),
                extra_info=f'El alumno ha sido reinscrito correctamente!'
            ))


@route('/alumno/baja')
@nav('Control Escolar/Baja')
@restricted(['EC2', 'ECA'])
def baja_alumno():
    """Renderiza la página de baja de alumno y obtiene los alumnos dependiendo del estado"""

    query = {"estado": session["estado"]}
    try:
        response = requests.post(CAPTACION_URL + '/get_alumnos_estado', json=query)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

    alumnos = microservice_data['result']
    lista_nombres_alumnos = [f"{alumno['nombre']} {alumno['apellido1']} {alumno['apellido2']}" for alumno in alumnos if 'estado' not in alumno.keys() ]
    return render_template('baja_alumno.html', estado=session['estado'], alumnos=lista_nombres_alumnos)

@route('/baja_alumno_bd', methods=['POST'])
def baja_alumno_bd():


    form_data = request.form.to_dict()
    nombre_completo = form_data['alumno']
    nombre_lista = nombre_completo.split()
    form_data["nombre"] = nombre_lista[0]
    form_data["apellido1"] = nombre_lista[1]
    form_data["apellido2"] = nombre_lista[2]

    try:
        response = requests.post(CAPTACION_URL + '/bajar_alumno', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    return make_response(render_template(f'success.html',
                stylesheets=['success', 'button'],
                title='Baja Concluida',
                redirect=url_for('baja_alumno'),
                extra_info=f'El alumno ha sido dado de baja exitosamente!'
            ))