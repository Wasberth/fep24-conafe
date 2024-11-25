from flask import render_template, request, redirect, url_for, session, flash, jsonify
from decos import route
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['captacion']
usuarios = db.formulario

@route('/login', methods=['GET'])
def login():
    """Renderiza el formulario del login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template(f'login.html', stylesheets = ['login'])

@route('/auth', methods=['POST'])
def auth():
    """Maneja el inicio de sesión utilizando el ID de registro y CURP."""

    if request.method == 'POST':
        registro_id = request.form['registro_id']
        curp = request.form['curp']

        try:
            usuario = usuarios.find_one({'_id': ObjectId(registro_id), 'curp': curp})
        except:
            return jsonify({"error": "Formato de _id inválido"}), 400
        
        if usuario:
            session['user_id'] = str(usuario['_id'])
            return redirect(url_for('dashboard'))
        else:
            return jsonify({"error": "id o CURP incorrectos."}), 400
    
    return render_template('login.html')

@route('/logout', methods=['POST'])
def logout():
    """Cierra sesión y redirige a la página de login"""
    session.pop('user_id', None)
    return redirect(url_for('login'))  