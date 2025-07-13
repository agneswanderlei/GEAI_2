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
        observacao,
        data_cadastro
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
                    observacao,
                    data_cadastro
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                matricula,
                nome,
                nome_guerra,
                cargo,quadro,
                setor,
                funcao,
                situacao,
                disponibilidade,
                codigo_agente,
                observacao,
                data_cadastro
            )
        )
        conexao.commit()
        st.success('Agente cadastrado com sucesso')
    except sqlite3.IntegrityError:
        st.error(f'A matrícula {matricula} já está cadastrada!')
    except Exception as e:
        st.error(f' Error ao cadastrar agente {e}')
    finally:
        conexao.close()

def buscar_dados(matricula):
    conn = conectardb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Agentes WHERE matricula = ?",(matricula)) # isso serve para buscar na tabela o agente que a matricula for passada.
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def atualizar_agente(matricula, nome, nome_guerra, cargo, quadro, setor, funcao, situacao, disponibilidade, codigo_agente, observacao):
    conn = conectardb()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Agentes
        SET nome = ?, nome_guerra = ?, cargo = ?, quadro = ?, setor = ?, funcao = ?, situacao = ?, disponibilidade = ?, codigo_agente = ?, observacao = ?
        WHERE matricula = ?
    """, (nome, nome_guerra, cargo, quadro, setor, funcao, situacao, disponibilidade, codigo_agente, observacao, matricula))
    conn.commit()
    conn.close()
def atualizar_cadastro(
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
        observacao,

):
    conn = conectardb()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Agentes SET matricula = ?, nome = ?, nome_guerra = ?, cargo = ?, quadro = ?, setor = ?, funcao = ?, situacao = ?, disponibilidade = ?, codigo_agente = ?, obervacao = ? 
    """,(
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
        observacao,
    ))

