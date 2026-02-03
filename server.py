from flask import Flask, Response, request, abort
import os
from cryptography.fernet import Fernet
import hashlib

app = Flask(__name__)

# Pre-generated secure keys
ENCRYPTION_KEY = b'8vHxJmK9ZQ7yN2pR5tFwL3jX6nB4mV8sA1cD9eG2hK0='
AUTH_TOKEN = 'xK9mP3vL2nR8qW5tY7jF4hD6sA1cB9eG3kM0pN2xZ8v'

fernet = Fernet(ENCRYPTION_KEY)

@app.route('/get-main')
def get_main():
    # Verify auth token
    token = request.headers.get('X-Auth-Token')
    if not token or hashlib.sha256(token.encode()).hexdigest() != hashlib.sha256(AUTH_TOKEN.encode()).hexdigest():
        abort(403)
    
    # Read and encrypt main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    encrypted = fernet.encrypt(code.encode())
    
    return Response(encrypted, mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
