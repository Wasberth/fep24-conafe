from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from __mongo_operations__ import objectid_to_str
import bson
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['CCT']

lugares = db['cct']
estados = db['estados_republica']

@app.route('/lista_lugares', methods=['GET']) 
def get_lugares():
    """Obtiene la lista de CCT."""
    # Checar si se envió un estado
    data = request.get_json(silent=True)
    query = {}
    if data is not None and 'estado' in data:
        query = {"estado": data['estado']}

    lugares_list = lugares.find(query)
    return jsonify(objectid_to_str({"result":list(lugares_list)}))

@app.route('/lista_lugares_estado', methods=['GET']) 
def get_lugares_estado():
    """Obtiene la lista de CCT por estado."""
    data = request.get_json()['estado']
    lugares_list = lugares.find({"estado": data})
    return jsonify(objectid_to_str({"result":list(lugares_list)}))

@app.route('/cot_estado', methods=['GET']) 
def get_estado_por_folio():
    """Obtiene el estado del COT"""
    data = request.get_json()['cot']
    estado = estados.find({"cot": data})
    return jsonify(objectid_to_str({"result":list(estado)}))

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)