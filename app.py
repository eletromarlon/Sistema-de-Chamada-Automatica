from email.policy import default
from flask import Flask, jsonify, redirect, render_template, request, url_for
from server_client_v2.db_operations import DatabaseManager
from server_client_v2.time_utils import TimeUtils

BANCO = 'sca_db'

db = DatabaseManager(BANCO)
DISCIPLINAS = db.read('Disciplina')

app = Flask(__name__)

def db_ops(name: str = BANCO):
        return DatabaseManager(name)

def listar_aulas(banco: str, codigo_disciplina: str):
    db = db_ops(banco)
    lista_aulas = db.read('Aula', {f'codigo_disciplina': str(codigo_disciplina)})
    return lista_aulas

def listar_frequencia(banco: str, id_aula: str):
    db = db_ops(banco)
    lista_presentes = db.read('Aula_Aluno', {'id_aula': id_aula})
    return lista_presentes

def listar_disciplinas(banco: str):
    db = db_ops(banco)
    lista_disciplinas = db.read('Disciplina')
    return lista_disciplinas

@app.route('/')
def login(name=None):
    return render_template('index.html', person=name)

@app.route('/home/', defaults={'cod_disciplina': None, 'id_aula': None, 'limpar':None}, methods=['GET'])
@app.route('/home/<cod_disciplina>', defaults={'id_aula': None, 'limpar':None}, methods=['GET'])
@app.route('/home/<cod_disciplina>/<id_aula>', defaults={'limpar':None}, methods=['GET'])
@app.route('/home/<cod_disciplina>/<id_aula>/<limpar>', methods=['GET'])
def home(cod_disciplina, id_aula, limpar):
    # Lista de disciplinas disponíveis
    disciplinas = DISCIPLINAS
    time = TimeUtils()

    # Listar aulas se o código da disciplina for fornecido
    if cod_disciplina:
        aulas = listar_aulas(banco=BANCO, codigo_disciplina=cod_disciplina)
        for aula, i in aulas, range(len(aulas)):
            temp = time.get_time_components(timestamp=aula[2])
            saida = ((str(temp['dia']) + str(temp['mes']) + str(temp['ano'])), 1)
            aula[i] = aula + saida
    else:
        aulas = []

    print(aulas)

    # Listar frequência se o ID da aula for fornecido
    if id_aula:
        tabela = listar_frequencia(banco=BANCO, id_aula=id_aula)
    else:
        tabela = [('-', '-', '-', '-')]
    
    if limpar:
        return redirect(f"/home/{cod_disciplina}")

    # Renderizar o template com os dados
    return render_template('home.html', aulas=aulas, tabela=tabela, disciplinas=disciplinas, cod_disciplina_select=cod_disciplina)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)  # Ativa o modo de depuração com recarregamento automático