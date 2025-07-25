import streamlit as st
import time
import sqlite3
from datetime import datetime

st.set_page_config('Excluir Setor',layout='centered')

# funções
def deletar_agentes(setorr):
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Vagas WHERE setor = ?",(setorr[0],))
    conn.commit()
    conn.close()
    st.success('Agente excluido com sucesso!',icon='✅')
    time.sleep(1)
    st.switch_page("paginas\Vagas\Home_Vagas.py")


@st.dialog('Atenção')
def deletar_msg(setorr):
    st.write(f'Deseja Excluir o Setor?')
    st.write(f'Setor: {setorr[0]}')
    st.write(f'Vagas: {setorr[1]}')
    st.markdown('<hr></hr>', unsafe_allow_html=True)
    if st.button('✅ Sim, Excluir!', key='botao_confir_delete'):
        deletar_agentes(setorr)



def listar_setor():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Vagas')
    data = cursor.fetchall()
    conn.close()
    return data

# Campo para digitar matrícula e botão de busca
st.header('Excluir Setor')
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
            vagas = st.number_input('Vagas', step=1, value=setorr[1], disabled=True)
        
        observacao = st.text_area('Observações',height=200, key='observacao', value=setorr[2], disabled=True)
        
        data_cadastro = datetime.now()
        submite = st.form_submit_button('Voltar')
        if submite:
            st.switch_page('paginas\Vagas\Home_Vagas.py')
            