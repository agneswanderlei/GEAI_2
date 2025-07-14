import streamlit as st
import os, sys
import time
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.funcoes_cadastro import buscar_dados, atualizar_cadastro,conectardb

options_cargo = [
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
]
options_quadro = [
    '',
    'QOPM',
    'QOAPM',
    'QPMG'
]
options_setor = [
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
]
options_funcao = [
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
]
options_situacao = [
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
]
options_disponibilidade = [
    '',
    'DISPONÍVEL',
    'INDISPONÍVEL',
]


def listar_policiais():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Agentes')
    data = cursor.fetchall()
    conn.close()
    return data

# Campo para digitar matrícula e botão de busca
st.subheader("🔍 Buscar Agente por Matrícula")
policiais = listar_policiais()
ids = [p[0] for p in policiais]

if 'matricula_default' not in st.session_state:
    st.session_state['matricula_default'] = ids[0]

id_selecionado = st.selectbox('Matricula', ids, index=ids.index(st.session_state['matricula_default']))
policial = next((p for p in policiais if p[0] == id_selecionado), None)


# formulário
st.markdown('<hr></hr>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns([1,1,2])
with col1:
    matricula = st.text_input('Matricula', key='matricula2',value=policial[0],disabled=True)
with col2:
    nome = st.text_input('Nome',value=policial[1],key='nome')
with col3:
    nome_guerra = st.text_input('Nome de Guerra',value=policial[2], key='nome_guerra')
with col4:
    cargo = st.selectbox(
        'Cargo',
        options_cargo,
        key='cargo',
        index=options_cargo.index(policial[3])
    )
with col5:
    quadro = st.selectbox(
        'Quadro',
        options_quadro,
        index=options_quadro.index(policial[4]),
        key='quadro'
    )
with col6:
    setor = st.selectbox(
        'Setor',
        options_setor,
        index=options_setor.index(policial[5]),
        key='setor'
    )
with col7:
    funcao = st.selectbox(
        'Função',
        options_funcao,
        index=options_funcao.index(policial[6]),
        key='funcao'
    )
with col8:
    disponibilidade = st.selectbox(
        'Disponibilidade',
        options_disponibilidade,
        index=options_disponibilidade.index(policial[8]),
        key='disponibilidade'
    )
with col9:
    situacao = st.selectbox(
        'Situação',
        options_situacao,
        index=options_situacao.index(policial[7]),
        key='situacao'
    )
observacao = st.text_area('Observação', value=policial[10], height=200, key='observacao')

botao_habilitado = False
if nome.strip() == '' or nome_guerra.strip() == '' or cargo =='' or quadro == '' or setor == '' or funcao == '' or disponibilidade == '' or situacao == '' or observacao == '':
    botao_habilitado = True
    st.warning('Todos os campos devem ser preenchidos!',icon='⚠️')
codigo_agente = 0
atualiar = st.button('Atualizar',disabled=botao_habilitado)
if atualiar:
    atualizar_cadastro(
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
        matricula
    )
    st.toast('✅ Agente atualizado com sucesso!')
    st.session_state['matricula_default'] = ids[0]  # Define como primeira matrícula
    time.sleep(1)
    st.switch_page("paginas\cadastro\Visualizar.py")
