import streamlit as st
import time
import sqlite3
st.set_page_config('Excluir Agentes',layout='wide')

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

def deletar_agentes(policial):
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Agentes WHERE matricula = ?",(policial[0],))
    conn.commit()
    conn.close()
    st.toast('Agente excluido com sucesso!',icon='✅')
    time.sleep(1)
    st.switch_page("paginas\cadastro\Home_Agentes.py")


def listar_policiais():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Agentes')
    data = cursor.fetchall()
    conn.close()
    return data

@st.dialog('Atenção')
def deletar_msg(policial):
    st.write(f'Deseja Excluir o Agente?')
    st.write(f'Matrícula: {policial[0]}')
    st.write(f'Cargo: {policial[3]}')
    st.write(f'Nome: {policial[1]}')
    st.markdown('<hr></hr>', unsafe_allow_html=True)
    if st.button('✅ Sim, Excluir!', key='botao_confir_delete'):
        deletar_agentes(policial)

# Campo para digitar matrícula e botão de busca
st.header('Excluir Agentes')
policiais = listar_policiais()
ids = [p[0] for p in policiais]
ids_sel = [p[5] for p in policiais]


id_selecionado = st.selectbox('Matricula', ids, help='"🔍 Buscar Agente por Matrícula"', placeholder='Digite a matricula.',format_func=lambda x: f'{x} - {next(p[1] for p in policiais if p[0]==x)}')
policial = next((p for p in policiais if p[0] == id_selecionado), None)


# formulário
st.markdown('<hr></hr>', unsafe_allow_html=True)
if policial:
    col1, col10, col11, col2, col3 = st.columns([1,1,1,3,2])
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns([1,1,2])
    with col1:
        matricula = st.text_input('Matricula', key='matricula2',value=policial[0],disabled=True)
    with col10:
        data_form = st.date_input('Data do Formulário', key='data_form',value=policial[9], disabled=True)
    with col11:
        num_form = st.text_input('Nº do Formulário', key='num_form', value=policial[10], disabled=True)
    with col2:
        nome = st.text_input('Nome',value=policial[1],key='nome',disabled=True)
    with col3:
        nome_guerra = st.text_input('Nome de Guerra',value=policial[2], key='nome_guerra',disabled=True)
    with col4:
        cargo = st.selectbox(
            'Cargo',
            options_cargo,
            key='cargo',
            index=options_cargo.index(policial[3],),
            disabled=True
        )
    with col5:
        quadro = st.selectbox(
            'Quadro',
            options_quadro,
            index=options_quadro.index(policial[4]),
            key='quadro',
            disabled=True
        )
    with col6:
        setor = st.selectbox(
            'Setor',
            ids_sel,
            index=ids_sel.index(policial[5]),
            key='setor',
            disabled=True
        )
    with col7:
        funcao = st.selectbox(
            'Função',
            options_funcao,
            index=options_funcao.index(policial[6]),
            key='funcao',
            disabled=True
        )
    with col8:
        situacao_agente = st.selectbox(
            'Situacao do Agente',
            options_situacao_agente,
            index=options_situacao_agente.index(policial[8]),
            key='situacao_agente',
            disabled=True
        )
    with col9:
        situacao = st.selectbox(
            'Situação',
            options_situacao,
            index=options_situacao.index(policial[7]),
            key='situacao',
            disabled=True
        )
    observacao = st.text_area('Observação', value=policial[10], height=200, key='observacao',disabled=True)
    nome = nome.upper()
    nome_guerra = nome_guerra.upper()

    codigo_agente = 0
    deletar = st.button('Deletar')
    if deletar:
        deletar_msg(policial)
else:
    st.warning('Agente não encontrado!')
