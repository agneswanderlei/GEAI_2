import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import os

st.set_page_config(layout='centered')
# Conexão com banco
def conecta_db():
    return sqlite3.connect(os.path.join('db','Geai.db'))

# Função para adicionar usuário
def adicionar_usuario(nome, username, perfil,senha_hash):
    conn = conecta_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Usuarios (nome, username, perfil, password)
            VALUES (?, ?, ?, ?)
            """,
            (nome, username, perfil, senha_hash)
        )
        conn.commit()
        st.success(f"✅ Usuário {username} adicionado com sucesso!")
    except sqlite3.IntegrityError:
        st.error("🚫 Esse nome de usuário já existe. Tente outro.")
    except Exception as e:
        st.error(f"❌ Erro ao adicionar usuário: {e}")
    finally:
        conn.close()

# UI da página
st.title("📋 Cadastro de Usuário")

with st.form("form_cadastro"):
    nome = st.text_input("Nome completo")
    username = st.text_input("Usuário", placeholder='Digite sua matrícula sem o hifen.')
    perfil = st.selectbox('Perfil',options=['admin','viewer'],index=1)
    senha = st.text_input("Senha", type="password")
    confirmar = st.text_input("Confirmar senha", type="password")
    enviar = st.form_submit_button("Cadastrar")

    if enviar:
        if senha != confirmar:
            st.warning("🔁 As senhas não coincidem.")
        elif not nome or not username or not senha:
            st.warning("📌 Todos os campos são obrigatórios.")
        else:
            senha_hash = stauth.Hasher.hash(senha)
            username = username.replace('-', '').strip()
            adicionar_usuario(nome, username, perfil, senha_hash)