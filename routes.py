from flask import request, jsonify
from json_utils import carrega_dados, salvar_Dados

def registrar_rotas(app):
    #Rota basica para testar o servidor
    @app.route('/')
    def home():
        return jsonify({"message":"Servidor flask está rodando e pronto para o CRUD!"})

    #Rota para add um novo aluno
    @app.route('/adiciona_aluno', methods=['POST'])
    def adicionar_aluno():
        dados = carrega_dados()

        if len(dados) == 0:
            nova_matricula = 1
        else:
            ultima_matricula = max(int(aluno['matricula']) for aluno in dados)
            nova_matricula = ultima_matricula + 1
            
        novo_aluno = request.get_json() #Esperamos um JSON com as informações do aluno, sem matrícula
        novo_aluno['matricula'] = str(nova_matricula)

        #add aluno a lista de dados
        dados.append(novo_aluno)
        salvar_Dados(dados)
        return jsonify({"message": "Aluno adicionado com sucesso!"}), 201
    
    #Rota para buscar alunos
    @app.route('/estudantes',methods=['GET'])
    def lista_alunos():
        dados = carrega_dados()
        return jsonify(dados)
    
    #Ver dados de um aluno em específico
    @app.route('/estudantes/<matricula>', methods=['GET'])
    def obter_aluno(matricula):
        dados = carrega_dados()
        aluno = next((aluno for aluno in dados if aluno['matricula'] == matricula),None)
        if aluno:
            boletim = aluno.get('boletim', {})
            media = {}
            status = {}
            
            valor_aprovacao = request.args.get('valor_aprovacao', default=7, type=float)

            for disciplina, notas in boletim.items():
                if len(notas) > 0:
                    media_diciplina = round(sum(notas) / len(notas), 1)
                    media[disciplina] = media_diciplina
                    
                    status[disciplina] = 'aprovado' if media_diciplina > valor_aprovacao else 'reprovado'
                else:
                    media[disciplina] = 0
                    status[disciplina] = 'reprovado'

            aluno_com_media = aluno.copy()
            aluno_com_media['medias'] = media
            aluno_com_media['status'] = status

            return jsonify(aluno_com_media), 200
        
        return jsonify({"message": "Aluno não encontrado"}), 404
    
        
    #Deleta um estudante
    @app.route('/deletar_estudante/<matricula>', methods=['DELETE'])
    def deletaEstudante (matricula):
        dados = carrega_dados()
        aluno_encontrado = False
        novos_dados = [aluno for aluno in dados if aluno['matricula'] != matricula]
        
        if len(novos_dados) < len(dados):
            aluno_encontrado = True
            
            if aluno_encontrado:
                salvar_Dados(novos_dados)
                return jsonify({"message": "Aluno removido com sucesso"}), 200
            else:
                return jsonify({"message": "Aluno não encontrado"}), 404
            
     #Atualiza o dado de um estudante       
    @app.route('/atualiza_estudante/<matricula>', methods=['PUT'])
    def atualiza_dados(matricula):
        dados = carrega_dados()
        aluno_encontrado = None
        
        for aluno in dados:
            if aluno['matricula'] == matricula:
                aluno_encontrado = aluno
                break
            
        if not aluno_encontrado:
            return jsonify({"message": "Aluno não encontrado"}), 404
        
        dados_atualizados = request.get_json()
        if not dados_atualizados:
            return jsonify({'message': 'Nenhum dado foi fornecido para ser atualizado'}), 400
            
        for chave, valor in dados_atualizados.items():
            if chave == 'boletim':
                for disciplina, notas in valor.items():
                    if disciplina in aluno_encontrado['boletim']:
                        #Se a displina já existir, adiciona as notas
                        aluno_encontrado['boletim'][disciplina].extend(notas)
                    else:
                        #Se a disciplina não existir, cria uma nova
                        aluno_encontrado['boletim'][disciplina] = notas
            elif chave in aluno_encontrado:
                #Atualiza qualquer outro campo
                aluno_encontrado[chave] = valor
                    
        salvar_Dados(dados)
        return jsonify({"message": "Aluno atualizado com sucesso", "aluno": aluno_encontrado}), 200 