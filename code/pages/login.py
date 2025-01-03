from flask import render_template, request, redirect, url_for, session, jsonify
from decos import route
import requests

from mode_handler import get_url
from pages._error_ import ConafeException

AUTENTICACION_URL = get_url('autenticacion')
CAPTACION_URL = get_url('captacion')

@route('/login', methods=['GET'])
def login():
    """Renderiza el formulario del login y redirige al usuario en caso de haber iniciado sesión"""
    if 'user_id' in session and 'nivel' in session:
        return redirect(url_for('wellcome'))
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
        raise ConafeException(500, "Error de conexión con el microservicio de autenticación.", str(e))
    
    usuario = microservice_data.get("user_id")
    nivel = microservice_data.get("nivel")
    user_id = microservice_data.get("real_id")

    #Validar si existe usuario
    if not usuario:
        raise ConafeException(401, "Usuario o contraseña incorrectos.")

    session['user_id'] = usuario
    session['nivel'] = nivel
    #session['real_id'] = str(user_id)
    
    try:
        sede_response = requests.post(CAPTACION_URL + '/sede', json={"nivel": nivel, "folio": usuario})
        sede_response.raise_for_status()
    except requests.RequestException as e:
        raise ConafeException(500, "Error de conexión con el microservicio de captación.", str(e))

    sede_response = sede_response.json()

    sede = sede_response.get('sede')
    if sede:
        session['sede'] = sede

    estado = sede_response.get('estado')
    if estado:
        session['estado'] = estado

    return redirect(url_for('wellcome'))
    
@route('/bienvenida')
def wellcome():
    """Renderiza la página de bienvenida"""
    return render_template(f'wellcome.html')
    
@route('/logout', methods=['POST'])
def logout():
    """Cierra sesión y redirige a la página de login"""
    session.clear()
    return redirect(url_for('login'))  