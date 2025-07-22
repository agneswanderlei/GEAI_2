import streamlit as st
import os, sys
import time
import sqlite3
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes_vagas import atualizar_vagas

st.set_page_config('Editar Setor',layout='centered')

# funções





def listar_setor():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Vagas')
    data = cursor.fetchall()
    conn.close()
    return data

# Campo para digitar matrícula e botão de busca
st.header('Editar Setor')
setores = listar_setor()
ids = [p[0] for p in setores]
ids_selecionado = st.selectbox('Setor', ids,key='setor_selecionado')
setorr = next((p for p in setores if p[0] == ids_selecionado), None)
print('teste',setorr)
# formulário
st.markdown('<hr></hr>', unsafe_allow_html=True)
if setores:
    with st.form('Cadastro de Agentes', clear_on_submit=True):
        col1, col2 = st.columns([2,1])
        with col1:
            setor = st.text_input('Setor',key='setor', value=setorr[0], disabled=True)
        with col2:
            vagas = st.number_input('Vagas', step=1, value=setorr[1], disabled=False)
        
        observacao = st.text_area('Observações',height=200, key='observacao', value=setorr[2])
        
        data_cadastro = datetime.now()
        submite = st.form_submit_button('Atualizar')
        if submite:
            
            if setor == '':
                st.toast('Por favor selecione um Setor!',icon='⚠️')
            
            if setor != '' :
                atualizar_vagas(
                    setor,
                    vagas,
                    observacao
                )