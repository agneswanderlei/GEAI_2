import streamlit as st
import os, sys
import time
import sqlite3
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from funcoes_cadastro import atualizar_cadastro
st.set_page_config('Editar Agentes',layout='wide')

# funções


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
    'AGUAR. RR',
    'LIC. ESPECIAL',
    'LIC. MATERNIDADE',
    'LIC. PATERNIDADE',
    'LIC. TRAT. INT. PART.',
    'LIC. TRAT. SAÚDE',
]
options_situacao_agente = [
    '',
    'APROVADO',
    'CADASTRADO',
    'CREDENCIADO',
    'DESCREDENCIADO',
    'FORMULÁRIO PRENCHIDO',
    'RECEBENDO GEAI',
]


def listar_policiais():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Agentes')
    data = cursor.fetchall()
    conn.close()
    return data
def listar_setores():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Vagas')
    data = cursor.fetchall()
    conn.close()
    return data

# Campo para digitar matrícula e botão de busca
st.header('Editar Agentes')
policiais = listar_policiais()
ids = [p[0] for p in policiais]
setores = listar_setores()
ids_sel = [p[0] for p in setores]

id_selecionado = st.selectbox('Matricula', ids,help='"🔍 Buscar Agente por Matrícula"', placeholder='Digite a matricula.',format_func=lambda x: f'{x} - {next(p[1] for p in policiais if p[0]==x)}')
policial = next((p for p in policiais if p[0] == id_selecionado), None)


# formulário
st.markdown('<hr></hr>', unsafe_allow_html=True)
if policial:
    col1, col10, col11, col2, col3 = st.columns(5)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns([1,1,2])
    with col10:
        data_form = st.date_input('Data do Formulário', key='data_form',value=policial[9], disabled=True)
    with col11:
        num_form = st.text_input('Nº do Formulário', key='num_form', value=policial[10], disabled=True)
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
            ids_sel,
            index=ids_sel.index(policial[5]),
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
        situacao_agente = st.selectbox(
            'Situacao do Agente',
            options_situacao_agente,
            index=options_situacao_agente.index(policial[8]),
            key='situacao_agente'
        )
    with col9:
        situacao = st.selectbox(
            'Situação',
            options_situacao,
            index=options_situacao.index(policial[7]),
            key='situacao'
        )
    observacao = st.text_area('Observação', value=policial[12], height=200, key='observacao')
    nome = nome.upper()
    nome_guerra = nome_guerra.upper()

    botao_habilitado = False
    if nome.strip() == '' or nome_guerra.strip() == '' or cargo =='' or quadro == '' or setor == '' or funcao == '' or situacao_agente == '':
        botao_habilitado = True
        st.warning('Todos os campos devem ser preenchidos!',icon='⚠️')
    codigo_agente = policial[11]
    atualiar = st.button('Atualizar',disabled=botao_habilitado)
    if atualiar:
        atualizar_cadastro(
            matricula,
            nome,
            nome_guerra,
            cargo,
            quadro,
            setor,
            funcao,
            situacao,
            situacao_agente,
            data_form,
            num_form,
            codigo_agente,
            observacao,
        )
        st.toast('✅ Agente atualizado com sucesso!')
        st.session_state['matricula_default'] = ids[0]  # Define como primeira matrícula
        time.sleep(1)
        st.switch_page(os.path.join('paginas','cadastro','Home_Agentes.py'))
else:
    st.warning('Agente não encontrado')