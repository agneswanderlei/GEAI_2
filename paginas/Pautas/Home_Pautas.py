import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
import io
st.set_page_config('Início',layout='centered')

# Funções
def listar_pautas():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pautas')
    data = cursor.fetchall()
    conn.close()
    return data
pautas = listar_pautas()
ids_pautas = [p[0] for p in pautas]

def listar_agentes():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, matricula FROM Agentes')
    data = cursor.fetchall()
    conn.close()
    return data
agentes = listar_agentes()
ids_agentes = [f'{p[1]} - {p[0]}' for p in agentes]

def buscar_dados():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT * FROM Pautas
        """
    )
    dados = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    df_pautas = pd.DataFrame(dados,columns=colunas)
    return df_pautas
df_pautas = buscar_dados()

# função para buscar pautas de agentes
def pautas_por_agentes(matriculas):
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT DISTINCT num_pauta FROM Agentes_pauta WHERE matricula IN ({",".join(["?" for _ in matriculas])})
        """,
        matriculas
    )
    pautas_result = cursor.fetchall()
    conn.close()
    pautas_r = [p[0] for p in pautas_result]
    return pautas_r

def pautas_por_situacao(situacoes):
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT DISTINCT num_pauta FROM Agentes_pauta WHERE situacao_agente IN ({",".join(['?' for _ in situacoes])})
        """,
        situacoes
    )
    pautas_result = cursor.fetchall()
    pautas_r = [p[0] for p in pautas_result]
    return pautas_r

# Formulario
st.subheader('Lista das Pautas 📋')
col1, col2 = st.columns([1,3])
col3, col4, col5 = st.columns(3)
with col1:
    pautas = st.multiselect('Pautas', ids_pautas)
with col2:
    agentes = st.multiselect('Agentes', ids_agentes)
with col3:
    situacao = st.multiselect('Situacao', ['Cadastro', 'Desligamento'])
with col4:
    data_inicio = st.date_input('Data Inicial', format='DD/MM/YYYY',value=None)
with col5:
    data_final = st.date_input('Data Final', format='DD/MM/YYYY', value=None)

# FILTROS
if pautas:
    df_pautas = df_pautas[df_pautas['num_pauta'].isin(pautas)]

df_pautas['data_envio'] = pd.to_datetime(df_pautas['data_envio'])
if data_inicio and data_final:
    df_pautas = df_pautas[
        (df_pautas['data_envio'].dt.date >= data_inicio) &
        (df_pautas['data_envio'].dt.date <= data_final)
    ]
df_pautas['data_envio'] = pd.to_datetime(df_pautas['data_envio']).dt.strftime('%d/%m/%Y')

if agentes:
    matriculas_selecionadas = [int(a.split(' - ')[0]) for a in agentes]
    pautas_selecionadas = pautas_por_agentes(matriculas=matriculas_selecionadas)
    df_pautas = df_pautas[df_pautas['num_pauta'].isin(pautas_selecionadas)]

if situacao:
    pautas_selecionadas = pautas_por_situacao(situacoes=situacao)
    df_pautas = df_pautas[df_pautas['num_pauta'].isin(pautas_selecionadas)]

# EXPORTAR PARA EXCEL
# criar um buffer na memoria
output = io.BytesIO()
# salvar df filtrado como arquivo excel
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_pautas[['num_pauta', 'data_envio', 'observacao']].to_excel(writer, index=False, sheet_name='Pautas')
# retorna ao inicio do buffer
output.seek(0)
st.download_button(
    "📤 Baixar Excel",
    data = output,
    file_name='Pautas.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
st.markdown(
    '<hr></hr>',unsafe_allow_html=True
)



# ALTERAR OS NOMES DAS COLUNAS DO DF
df_pautas = df_pautas.rename(
    columns={
        'num_pauta': 'Nº Pauta',
        'data_envio': 'Data de envio',
        'observacao': 'Observação'
    }
)

# DATAFRAME
st.dataframe(df_pautas[['Nº Pauta','Data de envio', 'Observação']])

