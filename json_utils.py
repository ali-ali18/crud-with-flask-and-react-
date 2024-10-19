import os
import json

CAMINHO_JSON = 'alunos.json'


def inicializa_json():
    if not os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, 'w') as f:
            json.dump([], f, indent=4)
            
def carrega_dados(): 
    inicializa_json()
    with open(CAMINHO_JSON, 'r') as f:
        return json.load(f)
    

def salvar_Dados(dados):
    with open(CAMINHO_JSON, 'w')as f:
        json.dump(dados, f, indent=4)
        
'''
inicializa_json
Faz a inicialização do json, caso o json não exista
no caminho mencionado, ele cria um json com um array vazio
'w' representa escrita
'''


'''
carrega_dados
Carrega os dados do arquivo JSON para o uso no código
ele inicializa o JSON para evitar erros caso ele não exista
Utilizamos with para abrir ele de forma segura e no modo leitura
apenas para receber os valores do json em formato de um dicionario
'r' representa leitura
'''