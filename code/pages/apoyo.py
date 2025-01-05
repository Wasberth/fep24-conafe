from flask import render_template, request, make_response, session, url_for, jsonify
from decos import route, nav
import requests
import base64
from mode_handler import get_url

from pages._check_level_ import restricted
from pages._error_ import ConafeException

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