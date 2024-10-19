from flask import Flask
from flask_cors import CORS
from json_utils import inicializa_json
from routes import registrar_rotas
#Inicia o flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"], "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": "*"}})

#incia a função verificação do json existe
inicializa_json()

#Incia as rotas 
registrar_rotas(app)

#Inicia a aplicação no modo depuração
if __name__ == '__main__':
    inicializa_json()
    app.run(debug=True)