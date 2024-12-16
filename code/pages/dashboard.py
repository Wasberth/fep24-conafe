from flask import render_template, request, redirect, url_for, session, jsonify
from decos import route
import requests
import json

from mode_handler import get_url

CAPTACION_URL = get_url('captacion')
AUTENTICACION_URL = get_url('autenticacion')
ACEPTACION_URL = get_url('aceptacion')


@route('/dashboard')
def dashboard():
    """Renderiza el panel de control y las convocatorias."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['nivel'] != "COT":
        return redirect(url_for('test_page'))

    # Obtener los datos del microservicio
    try:
        response = requests.get(ACEPTACION_URL + '/lista_convocatoria')
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
        
    microservice_data = json.loads(microservice_data)
    return render_template('dashboard.html', convocatorias=microservice_data)




@route('/convocatoria/<id>/aceptar', methods=['POST'])
def aceptar_convocatoria(id):
    """"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    convocatorias.update_one({'_id': ObjectId(id)}, {'$set': {'estado': 'aceptada'}})
    flash('Convocatoria aceptada', 'success')
    
    return redirect(url_for('dashboard'))

@route('/convocatoria/<id>/rechazar', methods=['POST'])
def rechazar_convocatoria(id):
    """"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    print("Rechazando ", id)
    
    convocatorias.update_one({'_id': ObjectId(id)}, {'$set': {'estado': 'rechazada'}})
    flash('Convocatoria rechazada', 'success')
    
    return redirect(url_for('dashboard'))
