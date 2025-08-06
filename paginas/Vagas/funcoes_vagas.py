import streamlit as st
import sqlite3
import time
import os

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

def inserir_vagas(setor, vagas, observacao):
    try:

        conn = sqlite3.connect(os.path.join('db','Geai.db'))
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Vagas(
                setor,
                vagas,
                observacao
            )
            VALUES (?, ?, ?)
        """,
        (setor, vagas, observacao)
        )
        conn.commit()
        st.success('Setor cadastrado com sucesso!')
        # time.sleep(1)
        # st.switch_page('paginas\Vagas\Home_Vagas.py')
    except sqlite3.IntegrityError:
        st.error('Setor já cadastrado')
    except Exception as e:
        st.error(f'Não foi possível caastrar setor {e}')
    finally:
        conn.commit()
        conn.close()

def atualizar_vagas(
        setor, vagas, observacao
):
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Vagas SET vagas = ?, observacao = ? WHERE setor = ?
    """, (vagas, observacao, setor)
    )
    conn.commit()
    conn.close()
    st.success('Setor atualizado com sucesso!')
    time.sleep(1)
    st.rerun()