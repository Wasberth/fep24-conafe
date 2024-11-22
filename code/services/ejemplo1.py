from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/list', methods=['GET'])
def get_list():
    """Returns a list of current date and time in JSON format."""
    data = [{'datetime': datetime.now().isoformat()}]
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5001)
