import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from funcoes_vagas import criar_tabela_vagas, inserir_vagas
from datetime import datetime

# Configuração pagina
st.set_page_config('Adicionar Vagas',layout='centered')
#  Carregar dados
criar_tabela_vagas()


st.header('Adicionar Vagas',width='content')
# Formulario do Cadastro de Vagas

with st.form('Cadastro de Agentes', clear_on_submit=True):
    col1, col2 = st.columns([2,1])

    with col1:
        setor = st.text_input('Setor',key='setor')
    with col2:
        vagas = st.number_input('Vagas', step=1)
    
    observacao = st.text_area('Observações',height=200, key='observacao')
    
    data_cadastro = datetime.now()
    submite = st.form_submit_button('Salvar')
    setor = setor.upper()
    if submite:
        
        if setor == '':
            st.toast('Por favor selecione um Setor!',icon='⚠️')
        
        if setor != '' :
            inserir_vagas(
                setor,
                vagas,
                observacao
            )