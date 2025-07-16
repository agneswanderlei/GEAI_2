import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.funcoes_cadastro import inserir_agente, conectardb
import time
import sqlite3
from datetime import datetime

st.header('Adicionar Agentes',width='content')
# Formulario do Cadastro de Agentes
if "matricula" not in st.session_state:
    st.session_state.matricula = ''
with st.form('Cadastro de Agentes', clear_on_submit=True):
    col1, col2, col3 = st.columns([1,2,1])
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns([1,1,2])
    with col1:
        matricula = st.text_input('Matricula', key='matricula')
    with col2:
        nome = st.text_input('Nome', key='nome')
    with col3:
        nome_guerra = st.text_input('Nome de Guerra', key='nome_guerra')
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
        ], key='cargo')
    with col5:
        quadro = st.selectbox('Quadro',
            [
                '',
                'QOPM',
                'QOAPM',
                'QPMG'
            ],key='quadro'
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

        ],key='setor')
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
        ],key='funcao')
    with col8:
        situacao_agente = st.selectbox('Situaçao do Agente',[
            '',
            'CADASTRADO',
            'CREDENCIADO',
            'DESCADASTRADO',
            'EFETIVADO',
        ],key='situacao_agente')
    with col9:
        situacao = st.selectbox('Situação',[
            '',
            'AGUAR. REG. EM SP',
            'AGUAR. RR',
            'FÉRIAS',
            'LIC. ESPECIAL',
            'LIC. MATERNIDADE',
            'LIC. PATERNIDADE',
            'LIC. TRAT. INT. PART.',
            'LIC. TRAT. SAÚDE',
            'REST. TRAT. SAÚDE',

        ], key='situacao')
    observacao = st.text_area('Observações',height=200, key='observacao')
    codigo_agente = 0
    data_cadastro = datetime.now()
    def limpar_matricula(matricula):
        return matricula.replace('-','').strip()
    matricula = limpar_matricula(matricula)
    nome = nome.upper()
    nome_guerra = nome_guerra.upper()
    submite = st.form_submit_button('Salvar')
    if submite:
        if matricula.strip() == '':
            st.toast('Por favor digite a Matricula!', icon='⚠️')
        if nome.strip() == '':
            st.toast('Por favor digite um Nome!', icon='⚠️')
        if nome_guerra.strip() == '':
            st.toast('Por favor digite um Nome de Guerra!', icon='⚠️')
        if cargo == '':
            st.toast('Por favor selecione um Cargo!', icon='⚠️')
        if quadro == '':
            st.toast('Por favor selecione um Quadro!',icon='⚠️')
        if setor == '':
            st.toast('Por favor selecione um Setor!',icon='⚠️')
        if funcao == '':
            st.toast('Por favor selecione uma Função!',icon='⚠️')
        if situacao_agente == '':
            st.toast('Por favor selecione uma Situação do Agente!',icon='⚠️')
        if matricula != '' and nome != '' and nome_guerra != '' and cargo != '' and quadro != '' and setor != '' and funcao != '' and situacao_agente != '':
            inserir_agente(
                matricula,
                nome,
                nome_guerra,
                cargo,
                quadro,
                setor,
                funcao,
                situacao,
                situacao_agente,
                codigo_agente,
                observacao,
                data_cadastro
            )