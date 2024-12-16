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
        # TODO: Los nombres de los campos de JSON no se deben quedar así jaja
        data = request.get_json()
        user = data.get('registro_id')
        password = data.get('curp')

        #Verificar si el usuario existe
        try:
            user = usuarios.find_one({'usuario': user, 'contraseña': password})
            
            #Validar si el curp coincide
            if user:
                # TODO: Corregir el id
                return jsonify({"nivel": str(user['nivel']), "user_id": str(user['_id'])})
            else:
                return jsonify({"error": "El usuario o la contraseña están incorrectas. Inténtelo de nuevo"}), 500
        except:
            return jsonify({"error": "Ocurrió un error al conectarse a la base de datos, inténtelo más tarde"}), 500
        
    

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)