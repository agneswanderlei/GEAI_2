import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import sqlite3
import pandas as pd
import io
st.set_page_config('Início',layout='wide')
from criar_tabelas import criar_tabela_agentes, criar_tabela_pautas, criar_tabela_vagas, criar_tabela_usuarios


# criar tabelas
criar_tabela_vagas()
criar_tabela_pautas()
criar_tabela_agentes()
criar_tabela_usuarios()

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


# definição de vagas
vagas_oficiais = 52
oficiais_cadastrados = 0
vagas_oficiais_preenchidas = 0
vagas_pracas = 325
pracas_cadastrados = 0
vagas_pracas_preenchidas = 0

def buscar_agentes():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute("SELECT data_form, num_form, matricula, nome, nome_guerra, cargo, quadro, setor, funcao, situacao_agente, situacao, codigo_agente, data_cadastro FROM Agentes")
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
        'funcao': 'Função',
        'situacao_agente': 'Situação do Agente',
        'situacao': 'Situação Extra',
        'codigo_agente': 'Código do Agente',
        'data_cadastro': 'Data do cadastro'
    })
    return dados

# consulta dados daas vagas na tabela
cursor = sqlite3.connect(os.path.join('db','Geai.db')).cursor()
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
ids = list(set([p for p in policiais['Setor']]))

st.title('Filtros')
# filtros
col7, col8, col9, col10 = st.columns(4)
col11, col14, col12, col13 = st.columns(4)
with col7:
    cargo = st.multiselect('Cargo',options_cargo)
with col8:
    quadro = st.multiselect('Quadro',options_quadro)
with col9:
    setor = st.multiselect('Setor',ids)
with col10:
    situacao_agente = st.multiselect('Situação do Agente',options_situacao_agente)
with col11:
    situacao = st.multiselect('Situacão Extra',options_situacao)
with col12:
    date_inicio = st.date_input('Data Início', value=None, format='DD/MM/YYYY')
with col13:
    date_fim = st.date_input('Data Fim', value=None, format='DD/MM/YYYY')
with col14:
    funcao = st.multiselect('Função',options_funcao)
    
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
if funcao:
    policiais = policiais[policiais['Função'].isin(funcao)]
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

st.dataframe(policiais.iloc[inicio:fim], use_container_width=True,)
# st.dataframe(policiais, use_container_width=True,)