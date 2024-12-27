from flask import render_template, request, redirect, url_for, session, jsonify, make_response
from decos import route, nav
import requests
import json

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._card_ import Card, CONVOCATORIA_TEMPLATE

CAPTACION_URL = get_url('captacion')
AUTENTICACION_URL = get_url('autenticacion')
ACEPTACION_URL = get_url('aceptacion')

@route('/dashboard')
@nav('Revisar Solicitudes')
@restricted('COT')
def dashboard():
    """Renderiza el panel de control y las convocatorias."""
    # Obtener los datos del microservicio
    try:
        response = requests.get(ACEPTACION_URL + '/lista_convocatoria', json={'cot_id': session['real_id']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
        
    microservice_data = microservice_data["result"]

    for i in range(len(microservice_data)):
        convocatoria = microservice_data[i]

        apellido = convocatoria['apellido1']
        if 'apellido2' in convocatoria and convocatoria['apellido2']:
            apellido += ' ' + convocatoria['apellido2']
        microservice_data[i]['apellido'] = apellido

        cuenta_bancaria = convocatoria['cuenta_bancaria']
        if 'clabe' in convocatoria and convocatoria['clabe']:
            cuenta_bancaria = convocatoria['clabe']
        microservice_data[i]['cuenta_bancaria'] = cuenta_bancaria

        direccion = convocatoria['direccion']
        if 'num_exterior' in convocatoria and convocatoria['num_exterior']:
            direccion += ' No. ' + convocatoria['num_exterior']
        else:
            direccion += ' S/N'

        if 'num_interior' in convocatoria and convocatoria['num_interior']:
            direccion += ' Interior ' + convocatoria['num_interior']
        microservice_data[i]['direccion'] = direccion

    cards = [Card.card_from_dict(CONVOCATORIA_TEMPLATE, **convocatoria) for convocatoria in microservice_data]
    return render_template('cartas.html', cards=cards, tipo_carta='carta_convocatoria', stylesheets=['button'])

@route('/convocatoria/<id>/<curp>/aceptar', methods=['POST'])
def aceptar_convocatoria(id, curp):
    """Acepta la convocatoria del aspirante y actualiza su estado."""
    #Declarar json con datos del usuario
    datos = {'usuario': id, 'contraseña':curp, 'nivel':'EC1'}

 # Obtener los datos del microservicio
    try:
        response = requests.post(ACEPTACION_URL + '/convocatoria/aceptar_bd', json=datos)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500

    # Obtener la ID del registro desde el microservicio
    nuevo_usuario = microservice_data.get('id')
    if not nuevo_usuario:
        return jsonify({"error": "El microservicio no retornó una ID válida"}), 500
    
    #Respuesta del servidor
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Convocatoria Aceptada',
                           redirect=url_for('dashboard'),
                           extra_info=f'La convocatoria ha sido aceptada con éxito, creando el usuario con el registro: {nuevo_usuario}'))
    
    return resp

@route('/convocatoria/<id>/rechazar', methods=['POST'])
def rechazar_convocatoria(id):
    """Rechaza la convocatoria del aspirante."""
    
    datos = {'_id': id}
    # Obtener los datos del microservicio
    try:
        response = requests.post(ACEPTACION_URL + '/convocatoria/rechazar_bd', json=datos)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500

    #Respuesta del servidor
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Convocatoria Rechazada',
                           redirect=url_for('dashboard'),
                           extra_info=f'La convocatoria ha sido rechazada con éxito. id del aspirante rechazado: {id}'))
    
    return resp