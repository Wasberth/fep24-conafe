from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from __mongo_operations__ import objectid_to_str
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

@app.route('/tallas', methods=['POST'])
def get_tallas():
    """Obtiene el registro de tallas de un año en específico"""	
    data = request.get_json()
    year = data['year']
    result = formulario.find({"convocatoria": year}, {'playera': 1, 'pantalon': 1, 'calzado':1})
    return jsonify(objectid_to_str({'result':list(result)}))

@app.route('/get_educadores', methods=['POST'])
def get_educadores():
    """Obtiene los educadores comunitarios en servicio (EC2) de un estado en específico"""
    data = request.get_json()
    estado = data['estado']

    result = formulario.find({"estado_republica": estado, "estado": "convenio"})
    print("resukt de get educadores: ", result)
    return jsonify(objectid_to_str({'result':list(result)}))

@app.route('/get_capacitacion', methods=['POST'])
def get_capacitacion():
    """Obtiene los educadores comunitarios en capacitacion (EC1) de un estado en específico"""
    data = request.get_json()
    estado = data['estado']

    result = formulario.find({"estado_republica": estado})
    return jsonify(objectid_to_str({'result':list(result)}))

@app.route('/get_alumnos_estado', methods=['POST'])
def get_alumnos_estado():
    """Obtiene a los alumnos por estado"""
    data = request.get_json()
    estado = data['estado']

    result = alumnos.find({"estado_republica": estado})
    return jsonify(objectid_to_str({'result':list(result)}))


@app.route('/buscar_integrante', methods=['POST'])
def get_integrante():
    """Obtiene los datos de una persona de la convocatoria usando folio"""
    data = request.get_json()
    query = data
    result = formulario.find_one(query)
    lista = []
    lista.append(result)
    return jsonify(objectid_to_str({'result': lista}))

@app.route('/registrar_apoyo', methods=['POST'])
def registrar_apoyo():
    """Registra un apoyo en la base de datos."""
    data = request.get_json()
    formulario.update_one({'folio': data['folio']}, {'$set': {'documentos_apoyo': data['documentos_apoyo'], 'estado_apoyo': 'revisando'}})
    return jsonify({"msg": "Éxito!"})

@app.route('/estado_apoyo', methods=['POST']) 
def get_estado_apoyo():
    """Regresa el estado del apoyo con base al folio del usuario"""
    data = request.get_json()
    query = {"folio": data['folio']}
    result = formulario.find_one(query)
    return jsonify({"estado_apoyo": result.get('estado_apoyo')}) if result else jsonify({"error": "No se encontró el registro"})

@app.route('/bajar_alumno', methods=['POST'])
def bajar_alumno():
    """Registra el estado del alumno como baja y su causa."""
    data = request.get_json()
    alumnos.update_one({'nombre': data['nombre'], 'apellido1': data['apellido1'], 'apellido2': data['apellido2'], "estado_republica": data['estado']}, {'$set': {'estado': "baja", 'causa_baja': data['causa_baja']}})
    return jsonify({"msg": "Éxito!"})

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)