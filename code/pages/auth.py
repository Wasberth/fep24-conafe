from flask import render_template, request, redirect, url_for, session, flash
from decos import route
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

uri = os.environ.get('MONGO_URI', 'mongodb+srv://fepi:n0m3l0@cluster.wdio0.mongodb.net/')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['captacion']
usuarios = db['usuarios']

@route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión utilizando el ID de registro y la CURP."""
    if request.method == 'POST':
        registro_id = request.form['registro_id']
        curp = request.form['curp']
        
        #cambiar el nombre por la variable equivalente en mongo db
        user = usuarios.find_one({'registro_id': registro_id, 'curp': curp})
        
        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            flash('ID de Registro o CURP incorrectos', 'error')
    
    return render_template('login.html')