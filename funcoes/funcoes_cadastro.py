import sqlite3
import streamlit as st

def conectardb():
    conexao = sqlite3.connect('./db/Geai.db')
    return conexao


#Criar Banco de Dados e tabelas


def inserir_agente(
        matricula,
        nome,
        nome_guerra,
        cargo,
        quadro,
        setor,
        funcao,
        situacao,
        disponibilidade,
        codigo_agente,
        observacao
):
    try:
        conexao = conectardb()
        cursor = conexao.cursor()
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
                    disponibilidade,
                    codigo_agente,
                    observacao
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (matricula, nome, nome_guerra, cargo, quadro, setor, funcao, situacao, disponibilidade, codigo_agente, observacao)
        )
        conexao.commit()
        st.success('Agente cadastrado com sucesso')
    except sqlite3.IntegrityError:
        st.error(f'A matrícula {matricula} já está cadastrada!')
    except Exception as e:
        st.error(f' Error ao cadastrar agente {e}')
    finally:
        conexao.close()

