import streamlit as st
import sys, os
import pandas as pd
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from funcoes_Pautas import criar_tabela_pautas, inserir_pautas, inserir_agentes_pautas
import time

# Configuração pagina
st.set_page_config('Adicionar Pautas',layout='centered')
#  Criar tabela caso nao exista
criar_tabela_pautas()
# Carregar dados dos agentes
conn = sqlite3.connect('./db/Geai.db')
cursor = conn.cursor()
cursor.execute(
    """
        SELECT matricula, nome FROM Agentes
    """
)
dados_agentes = cursor.fetchall()
opcoes_agentes = [f"{matricula} - {nome}" for matricula,nome in dados_agentes]

# Iniciar o estado
if 'agentes_pauta' not in st.session_state:
    st.session_state.agentes_pauta = []

# Formulario do Cadastro de Pauta
st.header('Adicionar Pauta',width='content')
col1, col2 = st.columns(2)
with col1:
    num_pauta = st.text_input('Número da pauta')
with col2:
    data_envio = st.date_input('Data de envio',format="DD/MM/YYYY")

# Formulário de adicionar agentes
st.subheader('Adicionar agentes')
col3, col4, col5 = st.columns([3,2,1])
with col3:
    agente_selecionado = st.selectbox('Agente', opcoes_agentes)
with col4:
    situacao = st.selectbox('Situação',['Cadastro', 'Desligamento'])
with col5:
    st.markdown('<br>',unsafe_allow_html=True) # isso serve para colocar o botao embaixo
    if st.button('➕'):
        st.session_state.agentes_pauta.append((agente_selecionado,situacao))
        print(st.session_state.agentes_pauta)
        

# mostrar agentes na tabela
df_agentes = pd.DataFrame(st.session_state.agentes_pauta,columns=['Agentes', 'Situação'])
df_editavel = st.data_editor(
    df_agentes,
    hide_index=True,
    num_rows='dynamic',
    disabled=['Agentes', 'Situação']
)
# Atualizar o estado após editar na tabela
st.session_state.agentes_pauta = df_editavel.to_records(index=False).tolist()
observacao = st.text_area('Observalçai',height=400)

# Botão salvar
if st.button('Salvar'):
    seucesso_pauta = inserir_pautas(num_pauta, data_envio, observacao)
    sucesso_agente = True
    if seucesso_pauta:
        for agente, situacao in st.session_state.agentes_pauta:
            matricula = int(agente.split(" - ")[0])
            if not inserir_agentes_pautas(num_pauta, matricula, situacao):
                sucesso_agente = False
        if sucesso_agente:
            st.toast("✅ Pauta e agentes salvos com sucesso!")
            time.sleep(2)
            st.session_state.agentes_pauta = []
            st.switch_page('paginas\Pautas\Home_Pautas.py')
