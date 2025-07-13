import sqlite3

conn = sqlite3.connect('./db/Geai.db')
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
        disponibilidade TEXT NOT NULL,
        codigo_agente TEXT NOT NULL,
        observacao TEXT NOT NULL,
        data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
)
conn.commit()
conn.close()