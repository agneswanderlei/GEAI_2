import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import os
st.set_page_config(layout='centered')

# Conexão com banco
def conecta_db():
    return sqlite3.connect(os.path.join('db','Geai.db'))

# Função para Editar usuário
def listar_usuarios():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios')
    data = cursor.fetchall()
    conn.close()
    return data

def atualizar_usuarios(
        username,
        password,
        
):
    conn = conecta_db()
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE Usuarios SET password = ? WHERE username = ?
        """,
        (
            password,
            username
        )
    )
    conn.commit()
    conn.close()

# -----Buscar Usuarios------
usuarios = listar_usuarios()
ids = [p[0] for p in usuarios]
id_selecionado = st.selectbox('Usuário', ids,help='"🔍 Buscar Agente por Matrícula"', placeholder='Digite a matricula.',format_func=lambda x: f'{x} - {next(p[2] for p in usuarios if p[0]==x)}')
usuario = next((p for p in usuarios if p[0] == id_selecionado), None)

# UI da página
st.title("📋 Editar Senha")

if usuario:
    with st.form("form_senha"):
        nome = st.text_input("Nome completo", disabled=True, value=usuario[1])
        username = st.text_input("Usuário", placeholder='Digite sua matrícula sem o hifen.', disabled=True,value=usuario[2])
        password = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirmar senha", type="password")
        enviar = st.form_submit_button("Atualizar")

        if enviar:
            if password != confirmar:
                st.warning("🔁 As senhas não coincidem.")
            elif not nome or not username or not password:
                st.warning("📌 Todos os campos são obrigatórios.")
            else:
                senha_hash = stauth.Hasher.hash(password)
                username = username.replace('-', '').strip()
                atualizar_usuarios(username, senha_hash)
                st.success('Usuario atualizado com sucesso!')
else:
    st.warning('Usuário não encontrado!')