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
        perfil
):
    conn = conecta_db()
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE Usuarios SET perfil = ? WHERE username = ?
        """,
        (
            perfil,
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
st.title("📋 Editar Peril")

if usuario:
    with st.form("form_pefil"):
        nome = st.text_input("Nome completo", disabled=True, value=usuario[1])
        username = st.text_input("Usuário", placeholder='Digite sua matrícula sem o hifen.', disabled=True,value=usuario[2])
        perfil = st.selectbox('Perfil',options=['admin','viewer'],index=['admin','viewer'].index(usuario[4]))
        enviar = st.form_submit_button("Atualizar")

        if enviar:
            username = username.replace('-', '').strip()
            atualizar_usuarios(username, perfil)
            st.success('Usuario atualizado com sucesso!')
else:
    st.warning('Usuário não encontrado!')