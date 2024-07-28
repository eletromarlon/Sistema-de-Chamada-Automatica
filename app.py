import datetime
from email.policy import default
from flask import Flask, flash, jsonify, redirect, render_template, render_template_string, request, url_for
from server_client_v2.db_operations import DatabaseManager
from server_client_v2.time_utils import TimeUtils
from dateutil import parser

BANCO = 'sca_db'

app = Flask(__name__)

def db_ops(name: str = BANCO):
    return DatabaseManager(name)

def listar_aulas(banco: str, codigo_disciplina: str):
    db = db_ops(banco)
    lista_aulas = db.read('Aula', {f'codigo_disciplina': str(codigo_disciplina)})
    db.close()
    return lista_aulas

def listar_frequencia(banco: str, id_aula: str):
    db = db_ops(banco)
    lista_presentes = db.read('Aula_Aluno', {'id_aula': id_aula})
    db.close()
    return lista_presentes

def listar_disciplinas(banco: str):
    db = db_ops(banco)
    lista_disciplinas = db.read('Disciplina')
    db.close()
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
    db = db_ops(BANCO)
    disciplinas = db.read('Disciplina')
    tempo = TimeUtils()
    button_disciplina = 'Disciplina'
    button_aula = 'Aula'

    # Listar aulas se o código da disciplina for fornecido
    if cod_disciplina:
        aulas = listar_aulas(banco=BANCO, codigo_disciplina=cod_disciplina)
        for aula, i in zip(aulas, range(len(aulas))):
            temp = tempo.get_time_components(timestamp=aula[2])
            lista = list(aula)
            lista.append(str(temp['dia']) + '/' + str(temp['mes']) + '/' + str(temp['ano']))
            aulas[i] = tuple(lista)
    else:
        aulas = []

    # Listar frequência se o ID da aula for fornecido
    if id_aula:
        tabela = listar_frequencia(banco=BANCO, id_aula=id_aula)
        button_disciplina = 'Limpe a tela'
        button_aula = 'Limpe a tela'
        disciplinas = [('-','-','-','-','-')]
        aulas = [('-','-','-','-','-')]
    else:
        tabela = [('-', '-', '-', '-')]
    
    if limpar:
        return redirect(f"/home/")

    # Renderizar o template com os dados setados
    return render_template(
            'home.html',
            button_disciplina=button_disciplina, 
            button_aula=button_aula, 
            aulas=aulas, 
            tabela=tabela, 
            disciplinas=disciplinas, 
            cod_disciplina_select=cod_disciplina
    )


app.secret_key = 'your_secret_key'  # Necessário para usar flash messages

@app.route('/cadastrar_aula', methods=['GET', 'POST'])
def cadastrar_aula():
    db = db_ops(BANCO)
    if request.method == 'POST':
        id_aula = request.form['id_aula']
        codigo_disciplina = request.form['codigo_disciplina']
        data_aula_str = request.form['data_aula']

        try:
            # Convertendo a data para timestamp usando dateutil.parser
            data_aula = parser.parse(data_aula_str)
            timestamp_aula = int(data_aula.timestamp())

            # Dados para inserção no banco
            data = {
                'id_aula': id_aula,
                'codigo_disciplina': codigo_disciplina,
                'data_aula': timestamp_aula
            }

            print(f'data comtem os dados {data}')

            # Inserindo no banco
            db.create('Aula', data)
            flash('Aula cadastrada com sucesso!', 'success')
            db.close()
            return redirect(url_for('cadastrar_aula'))
        except Exception as e:
            flash(f'Erro ao cadastrar aula: {e}', 'danger')
    
    return render_template('cadastrar_aula.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)  # Ativa o modo de depuração com recarregamento automático