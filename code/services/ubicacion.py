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

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)