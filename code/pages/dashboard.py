from flask import render_template, request, redirect, url_for, session, jsonify, make_response, Response
from decos import route, nav
import requests
import json
import base64
from mode_handler import get_url
from pages._check_level_ import restricted
from pages._card_ import Card, CONVOCATORIA_TEMPLATE, mapear_datos_convocatoria

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
        response = requests.get(ACEPTACION_URL + '/lista_convocatoria', json={'cot_id': session['user_id']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
        
    microservice_data = microservice_data["result"]

    convocatorias = mapear_datos_convocatoria(microservice_data)

    cards = [Card.card_from_dict(CONVOCATORIA_TEMPLATE, **convocatoria) for convocatoria in convocatorias]
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

@route('/convocatoria/documentos/<id>', methods=['GET'])
def mostrar_documentos(id):
    """Muestra los documentos del aspirante."""
    
    datos = {'_id': id}
    # Obtener los datos del microservicio
    try:
        response = requests.get(ACEPTACION_URL + '/convocatoria/documentos_necesarios', json=datos)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
    
    try:
        contenido_pdf = base64.b64decode(microservice_data["doc"]) if isinstance(microservice_data["doc"], str) else microservice_data["doc"]

        # Retornar el PDF con el encabezado adecuado
        return Response(contenido_pdf, mimetype='application/pdf')

    except Exception as e:
        return jsonify({"error": "Error al procesar el PDF", "details": str(e)}), 500