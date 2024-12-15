from flask import Flask, jsonify, request, render_template, request, redirect, url_for, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['login']

formulario = db['credenciales']
usuarios = db.credenciales

@app.route('/validacion_login', methods=['POST'])
def validacion_login():
    """Valida si el usuario ingresado existe en la base de datos y si las credenciales coinciden."""

    if request.method == 'POST':
        data = request.get_json()
        registro_id = data.get('registro_id')
        curp = data.get('curp')

        #Verificar si el usuario existe
        try:
            usuario = usuarios.find_one({'_id': ObjectId(registro_id)})
            
            #Validar si el curp coincide
            if str(curp) == str(usuario['curp']):
                return jsonify({"nivel": str(usuario['nivel']), "user_id": str(usuario['_id'])})
            else:
                return jsonify({"error": "Las contraseñas no coinciden."}), 500
        except:
            return jsonify({"error": "El usuario no existe."}), 500
        
    

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)