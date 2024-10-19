from flask import Flask
from json_utils import inicializa_json
from routes import registrar_rotas
#Inicia o flask
app = Flask(__name__)

#incia a função verificação do json existe
inicializa_json()

#Incia as rotas 
registrar_rotas(app)

#Inicia a aplicação no modo depuração
if __name__ == '__main__':
    inicializa_json()
    app.run(debug=True)