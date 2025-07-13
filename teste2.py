import sqlite3

conn = sqlite3.connect("gratificacoes.db")
cursor = conn.cursor()

# Tabela de policiais
cursor.execute("""
CREATE TABLE IF NOT EXISTS policiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

# Tabela de ofícios
cursor.execute("""
CREATE TABLE IF NOT EXISTS oficios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL,
    data TEXT
)
""")

# Tabela de associação
cursor.execute("""
CREATE TABLE IF NOT EXISTS oficio_policiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oficio_id INTEGER,
    policial_id INTEGER,
    FOREIGN KEY(oficio_id) REFERENCES oficios(id),
    FOREIGN KEY(policial_id) REFERENCES policiais(id)
)
""")

conn.commit()
conn.close()