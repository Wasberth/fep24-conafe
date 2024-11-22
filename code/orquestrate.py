from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/orchestrate', methods=['GET'])
def orchestrate():
    """Orchestrates responses from three microservices."""
    try:
        # Microservice 1: List with datetime
        list_response = requests.get('http://localhost:5001/list').json()

        # Microservice 2: Prime letters
        primes_response = requests.get('http://localhost:5002/primes').text

        # Microservice 3: Random number
        random_response = requests.get('http://localhost:5003/random').text

        # Combine results
        combined_response = {
            "datetime_list": list_response,
            "prime_letters": primes_response,
            "random_number": float(random_response)
        }
        return jsonify(combined_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='192.168.0.101', port=5000)
