import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
import io
st.set_page_config('Início',layout='wide')
st.header('Home Vagas',width='content')

# definição de options
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

def buscar_vagas():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT setor, vagas, observacao, data_cadastro FROM Vagas")
    colunas = [desc[0] for desc in cursor.description]
    vagas = cursor.fetchall()
    conn.close()
    df_vagas = pd.DataFrame(vagas, columns=colunas)
    return df_vagas

def contar_agentes_por_setor():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT setor, COUNT(*) as preenchidas
        FROM Agentes
        WHERE situacao_agente = 'RECEBENDO GEAI'
        GROUP BY setor
    """)
    dados = cursor.fetchall()
    conn.close()
    df_contagem = pd.DataFrame(dados, columns=['setor', 'preenchidas'])
    return df_contagem

vagas_df = buscar_vagas()
contagem_df = contar_agentes_por_setor()
tabela_final = vagas_df.merge(contagem_df, on='setor', how='left')
tabela_final['preenchidas'] = tabela_final['preenchidas'].fillna(0).astype(int)

# definição de vagas
vagas_oficiais = 52
oficiais_cadastrados = 0
vagas_oficiais_preenchidas = 0
vagas_pracas = 325
pracas_cadastrados = 0
vagas_pracas_preenchidas = 0

def buscar_agentes():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT data_form, num_form, matricula, nome, nome_guerra, cargo, quadro, setor, situacao_agente, situacao, codigo_agente, data_cadastro FROM Agentes")
    colunas = [desc[0] for desc in cursor.description] # nome das colunas
    policiais = cursor.fetchall()
    conn.close()
    dados = pd.DataFrame(policiais,columns=colunas)
    dados = dados.rename(columns={
        'data_form':'Data do Formulário',
        'num_form': 'Nº Formulário',
        'matricula': 'Matricula',
        'nome': 'Nome',
        'nome_guerra': 'Nome de Guerra',
        'cargo': 'Cargo',
        'quadro': 'Quadro',
        'setor': 'Setor',
        'situacao_agente': 'Situação do Agente',
        'situacao': 'Situação Extra',
        'codigo_agente': 'Código do Agente',
        'data_cadastro': 'Data do cadastro'
    })
    return dados

# consulta dados daas vagas na tabela
cursor = sqlite3.connect('./db/Geai.db').cursor()
cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN') AND situacao NOT IN ('DESCREDENCIADO')")
oficiais_cadastrados = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN') AND situacao NOT IN ('DESCREDENCIADO')")
pracas_cadastrados = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE situacao_agente = 'RECEBENDO GEAI' AND cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
vagas_oficiais_preenchidas = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE situacao_agente = 'RECEBENDO GEAI' AND cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
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
policiais = buscar_agentes()
st.title('Filtros')
# filtros
col7, col8, col9, col10, col11, col12, col13 = st.columns([1,1,1,2,2,1,1])
with col7:
    cargo = st.multiselect('Cargo',options_cargo)
with col8:
    quadro = st.multiselect('Quadro',options_quadro)
with col9:
    setor = st.multiselect('Setor',options_setor)
with col10:
    situacao_agente = st.multiselect('Situação do Agente',options_situacao_agente)
with col11:
    situacao = st.multiselect('Situacão Extra',options_situacao)
with col12:
    date_inicio = st.date_input('Data Início', value=None, format='DD/MM/YYYY')
with col13:
    date_fim = st.date_input('Data Fim', value=None, format='DD/MM/YYYY')
    
if cargo:
    policiais = policiais[policiais['Cargo'].isin(cargo)]
if quadro:
    policiais = policiais[policiais['Quadro'].isin(quadro)]
if setor:
    policiais = policiais[policiais['Setor'].isin(setor)]
if situacao_agente:
    policiais = policiais[policiais['Situação do Agente'].isin(situacao_agente)]
if situacao:
    policiais = policiais[policiais['Situação Extra'].isin(situacao)]
policiais['Data do Formulário'] = pd.to_datetime(policiais['Data do Formulário'])
if date_inicio and date_fim:
   policiais = policiais[
       (policiais['Data do Formulário'].dt.date >= date_inicio) &
       (policiais['Data do Formulário'].dt.date <= date_inicio)
   ]

# EXPORTAR PARA EXCEL
# criar um buffer na memoria
output = io.BytesIO()
# salvar df filtrado como arquivo excel
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    policiais.to_excel(writer, index=False, sheet_name='Agentes')
# retorna ao inicio do buffer
output.seek(0)
st.download_button(
    "📤 Baixar Excel",
    data = output,
    file_name='Agentes_filtrados.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
st.markdown('<hr></hr>',unsafe_allow_html=True)

por_paginas = 30
total_agentes = len(policiais)
# definir pagina atual
pagina_atual = st.number_input(
    'Página',
    min_value=1,
    max_value=(total_agentes // por_paginas) + 1,
    step=1,
    
)
inicio = (pagina_atual - 1) * por_paginas
fim = inicio + por_paginas

# st.dataframe(policiais.iloc[inicio:fim], use_container_width=True,)
# st.dataframe(policiais, use_container_width=True,)

st.subheader('Resumo de Vagas por Setor 📋')
st.dataframe(tabela_final[['setor', 'vagas', 'preenchidas']], use_container_width=True)