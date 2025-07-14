import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.funcoes_cadastro import inserir_agente, conectardb
import time
import sqlite3
from datetime import datetime

# definição de vagas
vagas_oficiais = 52
oficiais_cadastrados = 0
vagas_oficiais_preenchidas = 0
vagas_pracas = 352
pracas_cadastrados = 0
vagas_pracas_preenchidas = 0

# consulta dados daas vagas na tabela
cursor = sqlite3.connect('./db/Geai.db').cursor()
cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN') AND situacao NOT IN ('DESCREDENCIADO')")
oficiais_cadastrados = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN') AND situacao NOT IN ('DESCREDENCIADO')")
pracas_cadastrados = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE disponibilidade = 'DISPONÍVEL' AND situacao NOT IN ('DESCREDENCIADO', 'LIC. ESPECIAL', 'LIC. MATERNIDADE', 'LIC. TRAT. INT. PART.', 'LIC. TRAT. SAÚDE', 'CREDENCIADO') AND cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
vagas_oficiais_preenchidas = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE disponibilidade = 'DISPONÍVEL' AND situacao NOT IN ('DESCREDENCIADO', 'LIC. ESPECIAL', 'LIC. MATERNIDADE', 'LIC. TRAT. INT. PART.', 'LIC. TRAT. SAÚDE', 'CREDENCIADO') AND cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
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
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
with col1:
    card('Vagas de Oficias', vagas_oficiais,'#0d6efd')
with col2:
    card('Oficiais Cadastrado', oficiais_cadastrados,'#dc3545')
with col3:
    card('Vagas Preenchidas', vagas_oficiais_preenchidas,'#198754')
with col4:
    card('Vagas de Praças', vagas_pracas,'#0d6efd')
with col5:
    card('Praças Cadastrados', pracas_cadastrados,'#dc3545')
with col6:
    card('Vagas Preenchidas', vagas_pracas_preenchidas,'#198754')
st.markdown('<hr></hr>',unsafe_allow_html=True)

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
        disponibilidade = st.selectbox('Disponibilidade',[
            '',
            'DISPONÍVEL',
            'INDISPONÍVEL',
        ],key='disponibilidade')
    with col9:
        situacao = st.selectbox('Situação',[
            '',
            'AGUAR. REG. EM SP',
            'AGUAR. RR',
            'CREDENCIADO',
            'DESCREDENCIADO',
            'EFETIVADO',
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
        if disponibilidade == '':
            st.toast('Por favor selecione uma Disponibilidade!',icon='⚠️')
        if situacao == '':
            st.toast('Por favor selecione uma Situacao!',icon='⚠️')
        if matricula != '' and nome != '' and nome_guerra != '' and cargo != '' and quadro != '' and setor != '' and funcao != '' and disponibilidade != '' and situacao != '':
            inserir_agente(
                matricula,
                nome,
                nome_guerra,
                cargo,
                quadro,
                setor,
                funcao,
                situacao,
                disponibilidade,
                codigo_agente,
                observacao,
                data_cadastro
            )
            time.sleep(1)
            st.rerun()