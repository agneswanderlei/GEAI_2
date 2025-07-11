import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.funcoes_cadastro import inserir_agente, conectardb
import time
import sqlite3

# definição de vagas
vagas_oficiais = 52
vagas_oficiais_preenchidas = 0
vagas_pracas = 352
vagas_pracas_preenchidas = 0

# consulta dados daas vagas na tabela
cursor = sqlite3.connect('./db/Geai.db').cursor()
cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
vagas_oficiais_preenchidas = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
vagas_pracas_preenchidas = cursor.fetchall()[0][0]

# Estilos dos cards
def card(titulo, valor, cor='#f0f2f6'):
    st.markdown(
        f"""
        <div style="background-color:{cor}; padding:0px; border-radius:10px; text-align:center; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <h6 style="margin-bottom: 5px;">{titulo}</h6>
            <p style="margin-top: 0;">{valor}</p>
        </div>
        """, unsafe_allow_html=True
    )

# Layout cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    card('Vagas Oficias', vagas_oficiais,'#0d6efd')
with col2:
    card('Vagas Preenchidas', vagas_oficiais_preenchidas,'#198754')
with col3:
    card('Vagas Praças', vagas_pracas,'#ffc107')
with col4:
    card('Vagas Preenchidas', vagas_pracas_preenchidas,'#dc3545')

st.markdown('<hr></hr>',unsafe_allow_html=True)

# Formulario do Cadastro de Agentes
with st.form('Cadastro de Agentes', clear_on_submit=False):
    col1, col2, col3 = st.columns([1,2,1])
    col4, col5, col6, col7 = st.columns(4)
    with col1:
        matricula = st.text_input('Matricula')
    with col2:
        nome = st.text_input('Nome')
    with col3:
        nome_guerra = st.text_input('Nome de Guerra')
    with col4:
        cargo = st.selectbox('Cargo', [
            '',
            'CEL',
            'TC',
            'MAJ',
            'CAP',
            '1º TEN',
            '2º TEN',
            'SUB TEN',
            '1º SGT',
            '2º SGT',
            '3º SGT',
            'CB',
            'SD',
        ])
    with col5:
        quadro = st.selectbox('Quadro',
            [
                '',
                'QOPM',
                'QOAPM',
                'QPMG'
            ]
        )
    with col6:
        setor = st.selectbox('Setor', [
            '',
            'CHEFIA',
            'ADJUNTO',
            'SSA',
            'NTMB',
            'SS CSP',
            'SS PC',
            'NA',
            'NO',
            'PERMANÊNCIA',
            'TI',  
            'SS CCI',
            'SS CI',
            'CR I',
            'CR II',
            'CR III',
            'NIE',
            'ASI-7 / 1º BPM',
            'ASI-11 / 2º BPM',
            'ASI-19 / 3º BPM',
            'ASI-14 / 4º BPM',
            'ASI-26 / 5º BPM',
            'ASI-6 / 6º BPM',
            'ASI-24 / 7º BPM',
            'ASI-23 / 8º BPM',
            'ASI-18 / 9º BPM',
            'ASI-13 / 10º BPM',
            'ASI-5 / 11º BPM',
            'ASI-4 / 12º BPM',
            'ASI-2 / 13º BPM',
            'ASI-21 / 14º BPM',
            'ASI-1 / 16º BPM',
            'ASI-8 / 17º BPM',
            'ASI-10 / 18º BPM',
            'ASI-3 / 19º BPM',
            'ASI-9 / 20º BPM',
            'ASI-6 / 25º BPM',
            'ASI-8 / 26º BPM',
            'ASI-15 / 15º BPM',
            'ASI-12 / 21º BPM',
            'ASI-16 / 22º BPM',
            'ASI-17 / 24º BPM',
            'ASI-11 / 3ª CIPM',
            'ASI-12 / 5ª CIPM',
            'ASI-16 / 6ª CIPM',
            'ASI-15 / 8ª CIPM',
            'ASI-13 / 10ª CIPM',
            'ASI-20 / 23º BPM',
            'ASI-22 / 1ª CIPM',
            'ASI-25 / 2ª CIPM',
            'ASI-22 / 4ª CIPM',
            'ASI-25 / 7ª CIPM'

        ])
    with col7:
        funcao = st.selectbox('Função',[
            '',
            'ADJUNTO',
            'AG. DE BUSCA',
            'ANALISTA',
            'AUXÍLIAR ADM',
            'CHEFE', 
            'COORDENADOR',
            'GRADUADO',
            'MOTORISTA',
            'PERMANÊNCIA',
            'SECRETÁRIA'
        ])
    observacao = st.text_area('Observações',height=200)

    submite = st.form_submit_button('Salvar')
    if submite:
        if matricula == '':
            st.toast('Por favor digite a Matricula!', icon='⚠️')
        if nome == '':
            st.toast('Por favor digite um Nome!', icon='⚠️')
        if nome_guerra == '':
            st.toast('Por favor digite um Nome de Guerra!', icon='⚠️')
        if cargo == '':
            st.toast('Por favor selecione um Cargo!', icon='⚠️')
        if quadro == '':
            st.toast('Por favor selecione um Quadro!',icon='⚠️')
        if setor == '':
            st.toast('Por favor selecione um Setor!',icon='⚠️')
        if funcao == '':
            st.toast('Por favor selecione um Função!',icon='⚠️')
