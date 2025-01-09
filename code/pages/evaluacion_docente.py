from flask import render_template, request, redirect, url_for, session, jsonify, make_response
from decos import route, nav, offline
import requests
import json

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._decompose_form_ import decompose_form
from pages._error_ import ConafeException

CAPACITACION_URL = get_url('capacitacion')
CAPTACION_URL = get_url('captacion')

@route('/evaluacion/capacitacion')
@nav('Evaluación/Capacitación')
@offline()
@restricted('ECA')
def evaluacion_capacitacion():
    """Renderiza la página de evaluación al educador comunitario en capacitacion (EC1)"""
    try:
        response = requests.post(CAPTACION_URL + '/get_capacitacion', json={'estado':session['estado']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        captacion = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    if len(captacion['result']) == 0:
        raise ConafeException(404, f"No se encontraron educadores comunitarios en capacitación en el estado de {session['estado']}")

    datos_ec = [{"text":f"{ec['nombre']} {ec['apellido1']} {ec.get('apellido2', '')}", "value":ec['folio']} for ec in captacion['result']]
    print(datos_ec)

    return render_template(
        f'eval_capacitacion.html',
        stylesheets=['success', 'button'],
        scripts=['addEvaluationEC1'],
        estado = session['estado'],
        names = {'name':'folio', 'options':datos_ec}
    )

@route('/evaluacion/capacitacion_bd', methods=['POST'])
def evaluacion_capacitacion_bd():
    """Envía los datos del form al microservicio."""
    # Obtener los datos del formulario enviados por el cliente
    form_data = request.form.to_dict()
    form_data = {"registros":decompose_form(form_data)}
    
    # Enviar los datos al microservicio
    try:
        response = requests.post(CAPACITACION_URL + '/registrar_capacitacion', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

     # Crear la respuesta con la cookie
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Registro Concluido',
                           extra_info=f'Los registros se han guardado correctamente!'))

    return resp

@route('/evaluacion/servicio_bd', methods=['POST'])
def evaluacion_servicio_bd():
    """Envía los datos del form al microservicio."""
    # Obtener los datos del formulario enviados por el cliente
    form_data = request.form.to_dict()
    form_data = {"registros":decompose_form(form_data)}
    
    # Enviar los datos al microservicio
    try:
        response = requests.post(CAPACITACION_URL + '/registrar_servicio', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

     # Crear la respuesta
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Registro Concluido',
                           extra_info=f'Los registros se han guardado correctamente!'))

    return resp

@route('/evaluacion/servicio')
@nav('Evaluación/Servicio')
@offline()
@restricted('ECA')
def evaluacion_capacitacion_servicio():
    """Renderiza la página de evaluación al educador comunitario en servicio (EC2)"""
    try:
        response = requests.post(CAPTACION_URL + '/get_educadores', json={'estado':session['estado']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        captacion = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    if len(captacion['result']) == 0:
        raise ConafeException(404, f"No se encontraron educadores comunitarios en servicio en el estado de {session['estado']}")

    datos_ec = [
        {
            "text":f"{ec['nombre']} {ec['apellido1']} {ec.get('apellido2', '')}",
            "value":ec['folio']
        }
        for ec in captacion['result']
    ]

    """Renderiza la página de evaluación al educador comunitario en servicio (EC1)"""
    return render_template(
        f'eval_servicio.html',
        stylesheets=['success', 'button'],
        scripts=['addEvaluationEC2'],
        estado = session['estado'],
        names = {'name':'folio', 'options':datos_ec}
    )

