import sqlite3
import os

def criar_tabela_agentes():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Agentes (
            matricula INTEGER NOT NULL PRIMARY KEY,
            nome TEXT NOT NULL,
            nome_guerra TEXT NOT NULL,
            cargo TEXT NOT NULL,
            quadro TEXT NOT NULL,
            setor TEXT NOT NULL,
            funcao TEXT NOT NULL,
            situacao TEXT NOT NULL,
            situacao_agente TEXT NOT NULL,
            data_form TEXT NOT NULL,
            num_form TEXT NOT NULL,
            codigo_agente TEXT NOT NULL,
            observacao TEXT NOT NULL,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
    )
    conn.commit()
    conn.close()

def criar_tabela_pautas():

    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.executescript(
        """
            CREATE TABLE IF NOT EXISTS Pautas (
            num_pauta INTEGER PRIMARY KEY,
            data_envio TEXT NOT NULL,
            observacao TEXT NOT NULL,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
            CREATE TABLE IF NOT EXISTS Agentes_pauta (
            id INTEGER PRIMARY KEY,
            num_pauta INTEGER,
            matricula INTEGER,
            situacao_agente TEXT NOT NULL,
            FOREIGN KEY (num_pauta) REFERENCES Pautas(num_pauta)
            FOREIGN KEY (matricula) REFERENCES Agentes(matricula)
        );
    """
    )
    conn.commit()
    conn.close()

def criar_tabela_vagas():

    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Vagas (
        setor TEXT UNIQUE NOT NULL,
        vagas INTEGER NOT NULL,
        observacao TEXT NOT NULL,

        data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()

def criar_tabela_usuarios():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            username UNIQUE,
            password TEXT NOT NULL,
            perfil TEXT NOT NULL DEFAULT 'viewer'
            )  
        """
    )
    conn.close()