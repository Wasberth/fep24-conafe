from flask import render_template, request, jsonify, make_response
from decos import route
import requests

from mode_handler import get_url

CAPTACION_URL = get_url('captacion')

@route('/convocatoria')
def register_page():
    """Renderiza el formulario de la convocatoria para la captación de datos"""
    return render_template(f'convocatoria.html', stylesheets = ['capta'])

@route('/llenar_convocatoria', methods=['POST'])
def register_form():
    """Envía los datos del formulario al microservicio y guarda la ID en las cookies."""
    # Obtener los datos del formulario enviados por el cliente
    form_data = request.form.to_dict()
    
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