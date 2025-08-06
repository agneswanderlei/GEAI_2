import streamlit as st
import sys, os
import pandas as pd
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from funcoes_Pautas import excluir_pauta, criar_tabela_pautas
import time

# Configuração pagina
st.set_page_config('Excluir Pautas',layout='centered')
#  Criar tabela caso nao exista
criar_tabela_pautas()

# Carregar dados dos agentes
conn = sqlite3.connect(os.path.join('db','Geai.db'))
cursor = conn.cursor()
cursor.execute(
    """
        SELECT matricula, nome FROM Agentes
    """
)
dados_agentes = cursor.fetchall()
opcoes_agentes = [f"{matricula} - {nome}" for matricula,nome in dados_agentes]
conn.close()
# Buscar dados pautas
def listar_pautas():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT * FROM Pautas
        """
    )
    dados_pautas = cursor.fetchall()
    conn.close()
    return dados_pautas

def buscar_agentes_pautas(num_pauta):
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            Agentes.matricula,
            Agentes.nome,
            Agentes_pauta.situacao_agente
        FROM Agentes_pauta
        JOIN Agentes ON Agentes_pauta.matricula = Agentes.matricula
        WHERE Agentes_pauta.num_pauta = ?
        """,
        (num_pauta,)
    )
    resultado = cursor.fetchall()
    cursor.close()
    dados_formatados = [(f'{matricula} - {nome}', situacao) for matricula, nome, situacao in resultado]
    return dados_formatados

@st.dialog('Atenção')
def deletar_msg(dados_pautas_trat):
    st.write(f'Deseja Excluir a Pauta?')
    st.write(f'Nº Pauta: {dados_pautas_trat[0]}')
    st.markdown('<hr></hr>', unsafe_allow_html=True)
    if st.button('✅ Sim, Excluir!', key='botao_confir_delete'):
        excluir_pauta(dados_pautas_trat[0])
        time.sleep(2)
        st.switch_page(os.path.join('paginas','Pautas','Home_Pautas.py'))


# Iniciar o estado
if 'agentes_pauta_e' not in st.session_state:
    st.session_state.agentes_pauta_e = []
if 'pauta_carregada' not in st.session_state:
    st.session_state.pauta_carregada = None


# Formulario do Editar de Pauta
st.header('Excluir Pauta',width='content')
dados_pautas = listar_pautas()
ids = [p[0] for p in dados_pautas]
ids_selecionado = st.selectbox('Nº Pauta',ids, key='pauta_selecionada')
dados_pautas_trat = next((p for p in dados_pautas if p[0] == ids_selecionado), None)

st.markdown('<hr></hr>',unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    num_pauta = st.text_input('Número da pauta', disabled=True, value=dados_pautas_trat[0])
with col2:
    data_envio = st.date_input('Data de envio',format="DD/MM/YYYY", value=dados_pautas_trat[1],disabled=True)

# Formulário de adicionar agentes
st.subheader('Agentes Adicionados')



# Quando a pauta é selecionada, carregue os agentes para o estado
if 'agentes_pauta_e' not in st.session_state or st.session_state.pauta_carregada != ids_selecionado:
    st.session_state.agentes_pauta_e = buscar_agentes_pautas(ids_selecionado)
    st.session_state.pauta_carregada = ids_selecionado

# mostrar agentes na tabela
df_agentes = pd.DataFrame(st.session_state.agentes_pauta_e, columns=['Agentes', 'Situação'])
df_editavel = st.data_editor(
    df_agentes,
    hide_index=True,
    num_rows='fixed',
    disabled=['Agentes', 'Situação']
)

# 🔁 Aqui, atualiza o state
st.session_state.agentes_pauta_e = df_editavel.to_records(index=False).tolist()

# Atualizar o estado após editar na tabela
observacao = st.text_area('Observação',height=400, value=dados_pautas_trat[2],disabled=True)

# Botão salvar
if st.button('Excluir'):
    deletar_msg(dados_pautas_trat)
    