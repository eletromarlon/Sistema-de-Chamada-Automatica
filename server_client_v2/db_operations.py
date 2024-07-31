import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.executescript('''
                CREATE TABLE IF NOT EXISTS Curso (
                    codigo_curso TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    descricao TEXT
                );

                CREATE TABLE IF NOT EXISTS Professor (
                    matricula_professor TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    codigo_curso TEXT NOT NULL,
                    FOREIGN KEY (codigo_curso) REFERENCES Curso(codigo_curso)
                );

                CREATE TABLE IF NOT EXISTS Disciplina (
                    codigo_disciplina TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    carga_horaria INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Turma (
                    codigo_turma TEXT PRIMARY KEY,
                    codigo_curso TEXT NOT NULL,
                    semestre TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    FOREIGN KEY (codigo_curso) REFERENCES Curso(codigo_curso)
                );

                CREATE TABLE IF NOT EXISTS Aluno (
                    matricula_aluno TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    img_path TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Matricula (
                    id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricula_aluno TEXT NOT NULL,
                    codigo_turma TEXT NOT NULL,
                    data_matricula DATE NOT NULL,
                    FOREIGN KEY (matricula_aluno) REFERENCES Aluno(matricula_aluno),
                    FOREIGN KEY (codigo_turma) REFERENCES Turma(codigo_turma)
                );

                CREATE TABLE IF NOT EXISTS Aula (
                    id_aula TEXT PRIMARY KEY,
                    codigo_disciplina TEXT NOT NULL,
                    data_aula TEXT NOT NULL,
                    FOREIGN KEY (codigo_disciplina) REFERENCES Disciplina(codigo_disciplina)
                );

                CREATE TABLE IF NOT EXISTS Aula_Aluno (
                    id_frequencia INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricula_aluno TEXT NOT NULL,
                    id_aula INTEGER NOT NULL,
                    data_aula TIME NOT NULL,
                    presente BOOLEAN NOT NULL,
                    FOREIGN KEY (matricula_aluno) REFERENCES Aluno(matricula_aluno),
                    FOREIGN KEY (id_aula) REFERENCES Aula(id_aula)
                );

                -- Nova tabela que relaciona Professor com Disciplina
                CREATE TABLE IF NOT EXISTS Professor_Disciplina (
                    matricula_professor TEXT NOT NULL,
                    codigo_disciplina TEXT NOT NULL,
                    PRIMARY KEY (matricula_professor, codigo_disciplina),
                    FOREIGN KEY (matricula_professor) REFERENCES Professor(matricula_professor),
                    FOREIGN KEY (codigo_disciplina) REFERENCES Disciplina(codigo_disciplina)
                );

                -- Nova tabela que relaciona Disciplina com Turma
                CREATE TABLE IF NOT EXISTS Disciplina_Turma (
                    codigo_disciplina TEXT NOT NULL,
                    codigo_turma TEXT NOT NULL,
                    PRIMARY KEY (codigo_disciplina, codigo_turma),
                    FOREIGN KEY (codigo_disciplina) REFERENCES Disciplina(codigo_disciplina),
                    FOREIGN KEY (codigo_turma) REFERENCES Turma(codigo_turma)
                );
            ''')

    def create(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data.values())
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        with self.conn:
            self.conn.execute(sql, tuple(data.values()))

    def read(self, table, conditions=None):
        sql = f'SELECT * FROM {table}'
        if conditions:
            sql += ' WHERE ' + ' AND '.join(f"{k} = ?" for k in conditions.keys())
        with self.conn:
            cur = self.conn.execute(sql, tuple(conditions.values()) if conditions else ())
            return cur.fetchall()

    def update(self, table, data, conditions):
        """Atualiza uma tabela no banco de dados - Todos os parametros devem ser string

        Args:
            table (string): String contento o nome da tabela
            data (string): String com os dados a serem atualizados
            conditions (string): condiçoes da atualização
        
        Example:
            db.update('Curso', {'descricao': 'Engenharia de Software Atualizada'}, {'codigo_curso': 'CS101'})
        """
        updates = ', '.join(f"{k} = ?" for k in data.keys())
        conds = ' AND '.join(f"{k} = ?" for k in conditions.keys())
        sql = f'UPDATE {table} SET {updates} WHERE {conds}'
        with self.conn:
            self.conn.execute(sql, tuple(data.values()) + tuple(conditions.values()))

    def delete(self, table, conditions):
        conds = ' AND '.join(f"{k} = ?" for k in conditions.keys())
        sql = f'DELETE FROM {table} WHERE {conds}'
        with self.conn:
            self.conn.execute(sql, tuple(conditions.values()))

    def execute_query(self, query, params=()):
        with self.conn:
            cur = self.conn.execute(query, params)
            return cur.fetchall()

    def close(self):
        self.conn.close()
