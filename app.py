from flask import Flask, render_template
from server_client_v2.db_operations import DatabaseManager

app = Flask(__name__)

exemplo = [
    ['000000', 'Aluno 01', '01A'],
    ['000001', 'Aluno 02', '01A'],
    ['000002', 'Aluno 03', '01A'],
    ['000003', 'Aluno 04', '01A'],
    ['000004', 'Aluno 05', '02A'],
    ['000005', 'Aluno 06', '01A'],
    ['000006', 'Aluno 07', '01A'],
    ['000007', 'Aluno 08', '01A'],
    ['000008', 'Aluno 09', '04A'],
    ['000009', 'Aluno 10', '01A'],
    ['000010', 'Aluno 11', '01B'],
    ['000011', 'Aluno 12', '01A'],
    ['000012', 'Aluno 13', '01A'],
    ['000013', 'Aluno 14', '01A'],
    ['000014', 'Aluno 15', '03A'],
    ['000015', 'Aluno 16', '01A'],
    ['000016', 'Aluno 17', '06A'],
    ['000017', 'Aluno 18', '01A']
]

def db_ops(name: str = 'sca_db'):
        return DatabaseManager(name)

def header_table():
    header = ["Matricula", "Nome", "Turma"]
    return header

def table(disciplina: str = 'Matematica'):
    tabela = []
    for row in range(50):
        try:
            tabela.append(exemplo[row])
        except:
            tabela.append(['-', '-', '-'])
    return tabela

@app.route('/')
def login(name=None):
    return render_template('index.html', person=name)

@app.route('/home')
def home(name=None):
    frequencia = table()
    name = frequencia
    return render_template('home.html', tabela=name)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)  # Ativa o modo de depuração com recarregamento automático