from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/get-main')
def get_main():
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    return Response(code, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
