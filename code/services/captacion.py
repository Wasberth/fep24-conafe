from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bson
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
load_dotenv()

app = Flask(__name__)

uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['captacion']

formulario = db['formulario']
alumnos = db['alumnos']

db2 = client['CCT']
cct = db2['cct']
rep = db2['estados_republica']

@app.route('/registrar', methods=['POST'])
def get_list():
    """Registra un formulario en la base de datos y retorna la ID del registro."""
    data = request.get_json()

    #Asignar valor default a lengua en caso de no ser seleccionado
    if 'lengua' not in data:
        data['lengua'] = 'false'

    insert_result = formulario.insert_one(data)
    return jsonify({"id": str(insert_result.inserted_id)})

@app.route('/registrar_alumno', methods=['POST'])
def registrar_alumno():
    """Registra un formulario en la base de datos y retorna la ID del registro."""
    data = request.get_json()['registros']

    insert_result = alumnos.insert_many(data)
    return jsonify({"ids": str(insert_result.inserted_ids)})

@app.route('/estado', methods=['POST']) 
def get_estado():
    """Regresa el estado de un formulario en base a su ID y su curp"""
    data = request.get_json()
    query = {"_id": bson.ObjectId(data['id']), "curp": data['curp']}
    result = formulario.find_one(query)
    return jsonify({"estado": result.get('estado')}) if result else jsonify({"error": "No se encontró el registro"})

@app.route('/sede', methods=['POST'])
def get_sede():
    """Obtiene la sede de un Educador Comunitario según su nivel"""
    data = request.json
    nivel = data["nivel"]
    folio = data["folio"]

    if nivel == "COT":
        sede = rep.find_one({"cot":folio})
        return jsonify({'estado': sede["estado"]})
    elif nivel == "ECA":
        sede_id = formulario.find_one({"folio":folio})["sede"]
        sede = rep.find_one({"_id":ObjectId(sede_id)})
        return jsonify({'estado': sede["estado"]})
    elif nivel == "EC2":
        sede_id = formulario.find_one({"folio":folio})["sede"]
        sede = cct.find_one({"_id":ObjectId(sede_id)})
        return jsonify({'estado': sede["estado"].title(), 'sede': sede["clave"]})
    
    return jsonify({})

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)