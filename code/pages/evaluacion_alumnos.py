from flask import render_template, request, redirect, url_for, session, jsonify, make_response
from decos import route, nav, offline
import requests
import json

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._decompose_form_ import decompose_form
from pages._error_ import ConafeException

CAPTACION_URL = get_url('captacion')
CAPACITACION_URL = get_url('capacitacion')

@route('/evaluacion/alumnos')
@nav('Control Escolar/Calificar')
@offline()
@restricted('EC2')
def evaluacion_alumnos():
    """Renderiza la página de evaluación de los alumnos"""
    try:
        response = requests.post(CAPTACION_URL + '/get_alumnos_calif', json={'cct':session['sede']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        captacion = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    if len(captacion['result']) == 0:
        raise ConafeException(404, f"No se encontraron educadores comunitarios en capacitación en el estado de {session['estado']}")

    datos_ec = [{"text":f"{ec['nombre']} {ec['apellido1']} {ec.get('apellido2', '')}", "value":ec['folio']} for ec in captacion['result']]
    print(datos_ec)

    return render_template(
        f'eval_alumnos.html',
        stylesheets=['success', 'button', 'verticalText'],
        scripts=['addEvaluationStudent'],
        estado=session['estado'],
        cct=session['sede'],
        names={'name':'folio', 'options':datos_ec}
    )

@route('/evaluacion/alumnos_bd', methods=['POST'])
def evalucaion_alumnos_bd():
    """Envía los datos del form al microservicio."""
    # Obtener los datos del formulario enviados por el cliente
    form_data = request.form.to_dict()
    print(form_data)
    form_data = {"registros":decompose_form(form_data)}
    
    # Enviar los datos al microservicio
    try:
        response = requests.post(CAPACITACION_URL + '/registrar_calif_alumno', json=form_data)
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