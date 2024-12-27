from flask import render_template, request, redirect, url_for, session, jsonify
from decos import route
import requests

from mode_handler import get_url

AUTENTICACION_URL = get_url('autenticacion')

@route('/login', methods=['GET'])
def login():
    """Renderiza el formulario del login y redirige al usuario en caso de haber iniciado sesión"""
    if 'user_id' in session and 'nivel' in session and session['nivel'] == "COT":
        return redirect(url_for('dashboard'))
    return render_template(f'login.html', stylesheets = ['login'])

@route('/auth', methods=['POST'])
def auth():
    """Envía los datos del formulario al microservicio y redirecciona dependiendo del nivel del usuario."""
     # Obtener los datos del formulario enviados por el cliente
    form_data = request.form.to_dict()

    # Enviar los datos al microservicio
    try:
        response = requests.post(AUTENTICACION_URL + '/validacion_login', json=form_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        # TODO: Corregir la forma de mandar el error, matar el servicio no es viable xD
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
    
    usuario=microservice_data.get("user_id")
    nivel=microservice_data.get("nivel")
    user_id=microservice_data.get("real_id")

    #Validar si existe usuario
    if usuario:
        session['user_id'] = str(usuario)
        session['nivel'] = str(nivel)
        session['real_id'] = str(user_id)
        #Redireccionar dependiendo del nivel del usuario
        if session['nivel'] == "COT":
            return redirect(url_for('dashboard'))
        if session['nivel'] == "EC1":
            return redirect(url_for('test_page'))
    else:
        return jsonify({"error": "Error obteniendo respuesta de microservicio."}), 400
    
    
@route('/logout', methods=['POST'])
def logout():
    """Cierra sesión y redirige a la página de login"""
    session.clear()
    return redirect(url_for('login'))  