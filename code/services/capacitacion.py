from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bson
import os
from dotenv import load_dotenv
load_dotenv()

from __mongo_operations__ import objectid_to_str

app = Flask(__name__)

uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['capacitacion']

formulario = db['ec1']
formulario_servicio = db['ec2']

@app.route('/registrar_capacitacion', methods=['POST'])
def registrar_capacitacion():
    """Registra un formulario en la base de datos."""
    data = request.get_json()['registros']
    insert_result = formulario.insert_many(data)
    return jsonify({"ids": str(insert_result.inserted_ids)})

@app.route('/registrar_calif_alumno', methods=['POST'])
def registrar_calif_alumno():
    """Registra el formulario de calificacion de alumnos en la base de datos."""
    data = request.get_json()['registros']
    insert_result = formulario.insert_many(data)
    return jsonify({"ids": str(insert_result.inserted_ids)})

@app.route('/registrar_servicio', methods=['POST'])
def registrar_servicio():
    """Registra un formulario en la base de datos."""
    data = request.get_json()['registros']
    insert_result = formulario_servicio.insert_many(data)
    return jsonify({"ids": str(insert_result.inserted_ids)})

@app.route('/get_evaluaciones', methods=['POST'])
def get_evaluaciones():
    """Obtiene todas las evaluaciones según un folio"""
    folio = request.get_json()['folio']
    ec1 = list(formulario.find({"folio":folio}))
    ec1 = [{"tipo":"ec1", **ec} for ec in ec1]
    ec2 = list(formulario_servicio.find({"folio":folio}))
    ec2 = [{"tipo":"ec2", **ec} for ec in ec2]

    combined = sorted(ec1 + ec2, key=lambda x: x['fecha'])

    return jsonify(objectid_to_str({"result":combined}))

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)