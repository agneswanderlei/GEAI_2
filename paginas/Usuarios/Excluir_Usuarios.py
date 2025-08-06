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

def deletar_usuario(usuario):
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuarios WHERE username = ?",(usuario[2],))
    conn.commit()
    conn.close()
    st.toast('Usuário excluido com sucesso!',icon='✅')
    # time.sleep(1)
    # st.switch_page(os.path.join('paginas','cadastro','Home_Agentes.py'))

@st.dialog('Atenção')
def deletar_msg(usuario):
    st.write(f'Deseja Excluir o Usuário: {usuario[2]}?')
    st.write(f'Nome: {usuario[1]}')
    st.markdown('<hr></hr>', unsafe_allow_html=True)
    if st.button('✅ Sim, Excluir!', key='botao_confir_delete'):
        deletar_usuario(usuario)

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
st.title("📋 Excluir Usuário")

if usuario:
    with st.form("form_excluir"):
        nome = st.text_input("Nome completo", disabled=True, value=usuario[1])
        username = st.text_input("Usuário", placeholder='Digite sua matrícula sem o hifen.', disabled=True,value=usuario[2])
        enviar = st.form_submit_button("Excluir")

        if enviar:
            username = username.replace('-', '').strip()
            deletar_msg(usuario)
else:
    st.warning('Usuário não encontrado!')