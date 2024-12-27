from flask import render_template, request, jsonify, make_response
from decos import route
import requests
import base64

from mode_handler import get_url

CAPTACION_URL = get_url('captacion')

@route('/convocatoria')
def register_page():
    """Renderiza el formulario de la convocatoria para la captación de datos"""
    return render_template(f'convocatoria.html', stylesheets = ['capta'])

@route('/llenar_convocatoria', methods=['POST'])
def register_form():
    """Envía los datos del formulario al microservicio y guarda la ID en las cookies."""

    file = request.files['documentos-necesarios']
    pdf_content = file.read()

    # Codificar el archivo en Base64
    encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

    # Obtener los datos del formulario enviados por el cliente
    form_data = request.form.to_dict()

    form_data["documentos-necesarios"] = encoded_pdf
    
    
    # Enviar los datos al microservicio
    try:
        response = requests.post(CAPTACION_URL + '/registrar', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500

    # Obtener la ID del registro desde el microservicio
    registro_id = microservice_data.get("id")
    if not registro_id:
        return jsonify({"error": "El microservicio no retornó una ID válida"}), 500

    # Crear la respuesta con la cookie
    resp = make_response(render_template(f'success.html',
                           stylesheets=['success', 'button'],
                           title='Registro Concluido',
                           extra_info=f'El personal de CONAFE se comunicará contigo por los medios proporcionados. Para cualquier trámite recuerda guardar tu código de registro {registro_id}'))
    resp.set_cookie('token', registro_id)  # Guardar la ID en las cookies
    return resp

@route('/estado', methods=['POST'])
def check_status():
    """Verifica el estado de un registro en el microservicio."""
    # Obtener la CURP del formulario
    id = request.form.get('id')
    curp = request.form.get('curp')
    if not curp:
        return jsonify({"error": "No se proporcionó la CURP"}), 400

    # Enviar la petición al microservicio
    try:
        response = requests.post(CAPTACION_URL + '/estado', json={"id": id, "curp": curp})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
        print(microservice_data)
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500

    estado = microservice_data.get("estado")

    return render_template('estado_solicitud.html', estado=estado) if microservice_data else jsonify({"error": "No se encontró el registro"})