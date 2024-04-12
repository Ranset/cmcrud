from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    ip = request.remote_addr
    return f'<h1>CM inicializador Base de Datos</h1><br>ip: {ip}'

if __name__ == '__main__':
    app.run(debug=True)