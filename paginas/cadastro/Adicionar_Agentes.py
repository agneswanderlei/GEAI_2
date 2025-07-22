import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.funcoes_cadastro import inserir_agente, conectardb
import time
import sqlite3
from datetime import datetime
st.set_page_config('Adicionar',layout='wide')

def formulario_existe_ano(num_form, data_form):
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    ano = data_form.year
    cursor.execute("""
        SELECT 1 FROM Agentes
        WHERE num_form = ? AND strftime('%Y', data_form) = ?
        """, (num_form, str(ano)))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def listar_setor():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM Vagas'
    )
    setores = cursor.fetchall()
    conn.close()
    return setores
setores = listar_setor()
ids = [s[0] for s in setores]

st.header('Adicionar Agentes',width='content')
# Formulario do Cadastro de Agentes
if "matricula" not in st.session_state:
    st.session_state.matricula = ''

if setores:
    with st.form('Cadastro de Agentes', clear_on_submit=True):
        col3, col1, col2, col4, col5 = st.columns([1,1,1,3,1])
        col6, col7, col8 = st.columns(3)
        col9, col10, col11 = st.columns([1,1,2])

        with col1:
            data_form = st.date_input('Data do Formulário', key='data_form',value=datetime.now(), format='DD/MM/YYYY')
        with col2:
            num_form = st.text_input('Nº do Formulário', key='num_form')
        with col3:
            matricula = st.text_input('Matricula', key='matricula')
        with col4:
            nome = st.text_input('Nome', key='nome')
        with col5:
            nome_guerra = st.text_input('Nome de Guerra', key='nome_guerra')
        with col6:
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
        with col7:
            quadro = st.selectbox('Quadro',
                [
                    '',
                    'QOPM',
                    'QOAPM',
                    'QPMG'
                ],key='quadro'
            )
        with col8:
            setor = st.selectbox('Setor', ids)
        with col9:
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
        with col10:
            situacao_agente = st.selectbox('Situaçao do Agente',[
                '',
                'APROVADO',
                'CADASTRADO',
                'CREDENCIADO',
                'DESCREDENCIADO',
                'FORMULÁRIO PRENCHIDO',
                'RECEBENDO GEAI',
            ],key='situacao_agente')
        with col11:
            situacao = st.selectbox('Situação',[
                '',
                'AGUAR. RR',
                'LIC. ESPECIAL',
                'LIC. MATERNIDADE',
                'LIC. PATERNIDADE',
                'LIC. TRAT. INT. PART.',
                'LIC. TRAT. SAÚDE',
            ], key='situacao')
        observacao = st.text_area('Observações',height=200, key='observacao')
        
        data_cadastro = datetime.now()
        def limpar_matricula(matricula):
            return matricula.replace('-','').strip()
        matricula = limpar_matricula(matricula)
        nome = nome.upper()
        nome_guerra = nome_guerra.upper()
        submite = st.form_submit_button('Salvar')
        if submite:
            if data_form == '':
                st.toast('Por favor digite a Data do formulário!', icon='⚠️')
            if num_form.strip() == '':
                st.toast('Por favor digite o Número do formulário!', icon='⚠️')
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
            if matricula != '' and nome != '' and nome_guerra != '' and cargo != '' and quadro != '' and setor != '' and funcao != '' and situacao_agente != '' and num_form != '' and data_form != '':
                if formulario_existe_ano(num_form, data_form):
                    st.toast('Esse número de formulário já existe!', icon='🚫')
                else:
                    matricula = str(matricula)
                    quebra_nome = nome.split(' ')
                    letra1 = quebra_nome[0][0]
                    letra2 = quebra_nome[1][1]
                    letra3 = quebra_nome[-1][0]
                    letra4 = matricula[1]
                    letra5 = matricula[-2]
                    letra6 = matricula[-1]
                    codigo_agente = letra1 + letra2 + letra3 + letra4 + letra5 + letra6
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
                        data_form,
                        num_form,
                        codigo_agente,
                        observacao,
                        data_cadastro
                    )
else:
    st.warning('Setores não cadastrado! Favor cadastrar Setor!',icon='⚠️')