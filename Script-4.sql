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
    data_aula DATE NOT NULL,
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

-- Inserindo dados para teste
INSERT INTO Curso (codigo_curso, nome) VALUES 
('CC', 'Ciência da Computação'),
('EC', 'Engenharia Civil');

INSERT INTO Professor (matricula_professor, nome, sobrenome, email, codigo_curso) VALUES 
('150194', 'Tatiane', 'Silva', 'tatiane.silva@example.com', 'EC'),
('333333', 'Filipe', 'Souza', 'filipe.souza@example.com', 'CC');

INSERT INTO Aluno (matricula_aluno, nome, sobrenome, img_path) VALUES 
('210822', 'Ivo', 'Manoel', 'path/to/img1.jpg'),
('493408', 'Marlon', 'Silva', 'path/to/img2.jpg'),
('444444', 'Alan', 'Santos', 'path/to/img3.jpg'),
('555555', 'Angelina', 'Costa', 'path/to/img4.jpg'),
('210822', 'Ivo', 'Manoel', 'path/to/img1.jpg'),
('493408', 'Marlon', 'Silva', 'path/to/img2.jpg'),
('444444', 'Alan', 'Santos', 'path/to/img3.jpg'),
('555555', 'Angelina', 'Costa', 'path/to/img4.jpg'),
('499995', 'Zairo', 'Bastos', 'path/to/img1.jpg'),
('495811', 'Leticia', 'Torres', 'path/to/img.jpg'),
('495851', 'Gabriel', 'Rudan', 'path/to/img1.jpg'),
('555889', 'Fernanda', 'Scarcela', 'path/to/img1.jpg'),
('508700', 'Mikael', 'Sales', 'path/to/img1.jpg');

INSERT INTO Turma (codigo_turma, codigo_curso, semestre, ano) VALUES 
('01A', 'CC', '2024/1', 2024),
('02B', 'EC', '2024/1', 2024);

INSERT INTO Disciplina (codigo_disciplina, nome, descricao, carga_horaria) VALUES 
('DC', 'Desenho', 'Desenho técnico', 60),
('SD', 'Sistemas Distribuídos', 'Estudo de sistemas distribuídos', 80);

-- Relacionando Professores com Disciplinas
INSERT INTO Professor_Disciplina (matricula_professor, codigo_disciplina) VALUES 
('150194', 'DC'),
('333333', 'SD');

-- Relacionando Disciplinas com Turmas
INSERT INTO Disciplina_Turma (codigo_disciplina, codigo_turma) VALUES 
('DC', '02B'),
('SD', '01A');

INSERT INTO Aula (id_aula, codigo_disciplina, data_aula) VALUES
('DCA01', 'DC', '1721786400'),
('DCA02', 'DC', '1721872800'),
('DCA03', 'DC', '1721959200'),
('DCA04', 'DC', '1722045600'),
('DCA05', 'DC', '1722132000'),
('DCA06', 'DC', '1722218400'),
('DCA07', 'DC', '1721750400'),
('DCA08', 'DC', '1721836800'),
('DCA09', 'DC', '1721923200'),
('DCA010', 'DC', '1722009600'),
('DCA011', 'DC', '1722096000'),
('DCA012', 'DC', '1722182400');

INSERT INTO Aula (id_aula, codigo_disciplina, data_aula) VALUES
('SDA01', 'SD', '1721786400'),
('SDA02', 'SD', '1721872800'),
('SDA03', 'SD', '1721959200'),
('SDA04', 'SD', '1722045600'),
('SDA05', 'SD', '1722132000'),
('SDA06', 'SD', '1722218400'),
('SDA07', 'SD', '1721750400'),
('SDA08', 'SD', '1721836800'),
('SDA09', 'SD', '1721923200'),
('SDA010', 'SD', '1722009600'),
('SDA011', 'SD', '1722096000'),
('SDA012', 'SD', '1722182400');


INSERT INTO Aula_Aluno
(id_frequencia, matricula_aluno, id_aula, data_aula, presente)
VALUES(1, '493408', DCA01, '1721786400', 1);
INSERT INTO Aula_Aluno
(id_frequencia, matricula_aluno, id_aula, data_aula, presente)
VALUES(2, '210822', SDA01, '1721786400', 1);
INSERT INTO Aula_Aluno
(id_frequencia, matricula_aluno, id_aula, data_aula, presente)
VALUES(3, '493408', SDA01, '1721786400', 1);
INSERT INTO Aula_Aluno
(id_frequencia, matricula_aluno, id_aula, data_aula, presente)
VALUES(4, '444444', SDA01, '1721786400', 1);
INSERT INTO Aula_Aluno
(id_frequencia, matricula_aluno, id_aula, data_aula, presente)
VALUES(5, '555555', SDA01, '1721786400', 1);
