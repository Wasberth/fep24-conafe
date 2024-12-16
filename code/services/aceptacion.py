from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bson
from bson.json_util import dumps
import os
from dotenv import load_dotenv

from __mongo_operations__ import objectid_to_str

load_dotenv()

app = Flask(__name__)

# Configurar la conexión a MongoDB
uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['captacion']
convocatorias = db.formulario

@app.route('/lista_convocatoria', methods=['GET'])
def get_convocatoria_list():
    """Obtiene la lista de la convocatoria."""
    convocatorias_list = convocatorias.find({"estado":{"$exists": False}})
    return jsonify(objectid_to_str({"result":list(convocatorias_list)}))

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)