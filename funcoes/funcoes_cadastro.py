import sqlite3
import streamlit as st

#Criar Banco de Dados e tabelas
conexao = sqlite3.connect('./db/Geai.db')
cursor = conexao.cursor()
cursor.execute(
    """
        CREATE TABLE Agentes (
        matricula INTEGER NOT NULL PRIMARY KEY,
        nome TEXT NOT NULL,
        nome_guerra TEXT NOT NULL,
        cargo TEXT NOT NULL,
        quadro TEXT NOT NULL,
        setor TEXT NOT NULL,
        funcao TEXT NOT NULL,
        situacao TEXT NOT NULL,
        disponibilidade TEXT NOT NULL,
        data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
)
cursor.close()

def inserir_agente(
        matricula,
        nome,
        nome_guerra,
        cargo,
        quadro,
        setor,
        funcao,
        situacao,
        disponibilidade
):
    try:
        cursor.execute(
            """
                INSERT INTO Agentes(
                    matricula,
                    nome,
                    nome_guerra,
                    cargo,
                    quadro,
                    setor,
                    funcao,
                    situacao,
                    disponibilidade
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (matricula, nome, nome_guerra, cargo, quadro, setor, funcao, situacao, disponibilidade)
        )
        conexao.commit()
        st.success('Agente cadastrado com sucesso')
    except sqlite3.IntegrityError:
        st.error(f'A matrícula {matricula} já está cadastrada!')
    except Exception as e:
        st.error(f' Error ao cadastrar agente {e}')
    finally:
        conexao.close()

