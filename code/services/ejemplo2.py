from flask import Flask

app = Flask(__name__)

@app.route('/primes', methods=['GET'])
def get_prime_letters():
    """Returns a string of prime-indexed letters of the alphabet."""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    prime_letters = ''.join(alphabet[i - 1] for i in primes)
    return prime_letters

if __name__ == '__main__':
    app.run(port=5002)
