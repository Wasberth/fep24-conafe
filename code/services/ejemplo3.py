from flask import Flask
import random

app = Flask(__name__)

@app.route('/random', methods=['GET'])
def get_random_number():
    """Returns a random number between 0 and 1."""
    return str(random.random())

if __name__ == '__main__':
    app.run(port=5003)
