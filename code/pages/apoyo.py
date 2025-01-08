from flask import render_template, request, make_response, session, url_for, jsonify, Response
from decos import route, nav
import requests
import base64
from mode_handler import get_url

from pages._check_level_ import restricted
from pages._error_ import ConafeException
from pages._card_ import Card, APOYO_TEMPLATE, mapear_datos_convocatoria

ACEPTACION_URL= get_url('aceptacion')
CAPTACION_URL = get_url('captacion')

@route('/apoyo')
@nav('Apoyo/Solicitud')
@restricted(['EC1', 'EC2', 'ECA'])
def apoyo_estudios():
    folio = {"folio": session['folio']}
    # Enviar los datos al microservicio
    try:
        response = requests.post(CAPTACION_URL + '/buscar_integrante', json=folio)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        persona = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    persona = persona['result'][0]

    if "documentos_apoyo" in persona.keys():
        resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Apoyo Concluido',
                           extra_info=f'Ya has ingresado un apoyo en este ciclo escolar!. Para revisar el estado de tu apoyo da clic <a href="/apoyo/peticion">aquí</a>'))
        return resp
    return render_template(f'apoyo.html', stylesheets=['button'])

@route('/apoyo/peticion')
@nav('Apoyo/Peticiones')
@restricted(['EC1', 'EC2', 'ECA'])
def apoyo_peticion():
    """Revisa el estado del apoyo"""

    # Enviar la petición al microservicio
    try:
        response = requests.post(CAPTACION_URL + '/estado_apoyo', json={"folio": session['folio']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    estado = microservice_data.get("estado_apoyo")

    return render_template('estado_apoyo.html', estado_apoyo=estado) if microservice_data else jsonify({"error": "No se encontró el registro"})

@route('/apoyo/solicitud', methods=['POST'])
def iniciando_apoyo():
    form_data = request.form.to_dict()

    file = request.files['documentos_apoyo']
    pdf_content = file.read()

    # Codificar el archivo en Base64
    encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

    form_data["documentos_apoyo"] = encoded_pdf
    form_data["folio"] = session['folio']
    
    print("folio", session['folio'])
    # Enviar los datos al microservicio (actualizar convocatoria)
    try:
        response = requests.post(CAPTACION_URL + '/registrar_apoyo', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

    #Respuesta del servidor
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Solicitud de apoyo enviada!',
                           redirect=url_for('wellcome'),
                           extra_info=f'La solicitud de apoyo se ha enviado con éxito!'))
    
    return resp


@route('/ApoyoCIDAP')
@nav('Apoyos')
@restricted('CIDAP')
def apoyo_cidap():
    # Enviar los datos al microservicio (obtención de integrante)
    try:
        response = requests.post(CAPTACION_URL + '/get_solicitudes_apoyo', json={'estado_apoyo': "revisando"})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        personas = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
    
    
    apoyos = personas['result']
    
    apoyos_mapeados = mapear_datos_convocatoria(apoyos)


    cards = [Card.card_from_dict(APOYO_TEMPLATE, **apoyo, fecha_solicitud="10-12-2000") for apoyo in apoyos_mapeados]
    return render_template('cartas.html', cards=cards, tipo_carta='carta_apoyo', stylesheets=['button'])

@route('/aceptar_apoyo/<folio>', methods=['POST'])
def aceptar_apoyo(folio):
    """Acepta el apoyo y actualiza su estado"""
    #Declarar json con datos del usuario
    form_data = request.form.to_dict()
    form_data['folio'] = folio
 # Obtener los datos del microservicio
    try:
        response = requests.post(ACEPTACION_URL + '/aceptar_apoyo_bd', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
    
    #Respuesta del servidor
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Apoyo Aceptado',
                           redirect=url_for('apoyo_cidap'),
                           extra_info=f'El apoyo se ha aceptado con éxito!'))
    return resp

@route('/rechazar_apoyo/<folio>', methods=['POST'])
def rechazar_apoyo(folio):
    """Rechaza el apoyo y actualiza su estado"""
    #Declarar json con datos del usuario
    form_data = request.form.to_dict()
    form_data['folio'] = folio
 # Obtener los datos del microservicio
    try:
        response = requests.post(ACEPTACION_URL + '/rechazar_apoyo_bd', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
    
    #Respuesta del servidor
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Apoyo Rechazado',
                           redirect=url_for('apoyo_cidap'),
                           extra_info=f'El apoyo se ha rechazado con éxito!'))
    return resp

@route('/apoyo/documentos/<folio>', methods=['GET'])
def mostrar_documentos_apoyo(folio):
    """Muestra los documentos del aspirante."""
    
    datos = {'folio': folio}
    # Obtener los datos del microservicio
    try:
        response = requests.get(ACEPTACION_URL + '/apoyo/documentos_necesarios', json=datos)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    try:
        contenido_pdf = base64.b64decode(microservice_data["doc"]) if isinstance(microservice_data["doc"], str) else microservice_data["doc"]

        # Retornar el PDF con el encabezado adecuado
        return Response(contenido_pdf, mimetype='application/pdf')

    except Exception as e:
        raise ConafeException(422, "Error al procesar el PDF, porfavor intente subir otro archivo", str(e))