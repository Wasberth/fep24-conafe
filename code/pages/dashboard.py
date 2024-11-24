from flask import render_template, request, redirect, url_for, session, flash
from decos import route
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

# Configurar la conexión a MongoDB
uri = os.environ.get('MONGO_URI', 'mongodb+srv://fepi:n0m3l0@cluster.wdio0.mongodb.net/')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['captacion']
convocatorias = db['convocatorias']

@route('/dashboard')
def dashboard():
    """Muestra el panel de control para visualizar y aceptar/denegar formatos de convocatoria."""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    convocatorias_list = list(convocatorias.find())
    
    return render_template('dashboard.html', convocatorias=convocatorias_list)

@route('/convocatoria/<id>/aceptar', methods=['POST'])
def aceptar_convocatoria(id):
    """Acepta una convocatoria."""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    convocatorias.update_one({'_id': id}, {'$set': {'estado': 'aceptada'}})
    flash('Convocatoria aceptada', 'success')
    
    return redirect(url_for('dashboard'))

@route('/convocatoria/<id>/rechazar', methods=['POST'])
def rechazar_convocatoria(id):
    """Rechaza una convocatoria."""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    convocatorias.update_one({'_id': id}, {'$set': {'estado': 'rechazada'}})
    flash('Convocatoria rechazada', 'success')
    
    return redirect(url_for('dashboard'))