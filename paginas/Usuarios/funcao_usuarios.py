import sqlite3
import os
import streamlit as st
def conecta_db():
    conn = sqlite3.connect(os.path.join('Geai.db'))
    return conn

def inserir_user(nome, username, password, perfil):
    conn = conecta_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
                INSERT INTO Usuarios 
                (nome,
                username,
                password,
                perfil)
                VALUES (?, ?, ?, ?)
            """, (nome, username, password, perfil)
        )
        conn.commit()
        conn.close()
        st.success('Usuário gravado com Sucesso!')
    except sqlite3.IntegrityError:
        st.error(f'Usuario {username} já cadastrado')
    except Exception as e:
        st.error(f'Não foi possícel cadastrar usuario {e}')
    finally:
        conn.close()

def consulta_user():
    conn =conecta_db()
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT * FROM Usuarios
        """
    )
    dados = cursor.fetchall()
    return dados