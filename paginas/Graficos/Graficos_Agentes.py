import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config('Gráficos dos Agentes', layout='wide')
st.header('📊 Gráficos de Agentes')

def carregar_dados():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    df = pd.read_sql_query("SELECT * FROM Agentes", conn)
    conn.close()
    return df

df = carregar_dados()
print(df.columns)
# Filtro por setor (opcional)
setores = df['setor'].unique().tolist()
setor_selecionado = st.selectbox('Filtrar por Setor', ['Todos'] + setores)
if setor_selecionado != 'Todos':
    df = df[df['setor'] == setor_selecionado]

# Gráfico de setores
fig_setores = px.bar(
    df['setor'].value_counts().reset_index(),
    x='setor',
    y='count',
    labels={'count': 'Quantidade', 'setor': 'Setores'},
    title='Setores',
    color='setor'
)

# Gráfico de barras por Cargo
fig_cargo = px.bar(
    df['cargo'].value_counts().reset_index(),
    x='cargo',
    y='count',
    labels={'count': 'Quantidade', 'cargo': 'Cargo'},
    title='Total de Agentes por Cargo',
    color='cargo'
)

# Gráfico de pizza por Função
fig_funcao = px.pie(
    df,
    names='funcao',
    title='Distribuição por Função',
    hole=0.4
)
print(df['situacao'].value_counts().reset_index())

# Gráfico de barras por Situação
fig_situacao = px.bar(
    df['situacao_agente'].value_counts().reset_index(),
    x='situacao_agente',
    y='count',
    labels={'count': 'Quantidade', 'situacao_agente': 'Situação do Agente'},
    title='Situação dos Agentes',
    color='situacao_agente'
)
# Gráfico de barras por Quadro
fig_quadro = px.bar(
    df['quadro'].value_counts().reset_index(),
    x='quadro',
    y='count',
    labels={'count': 'Quantidade', 'quadro': 'Agentes por quadros'},
    title='Quadros dos Agentes',
    color='quadro'
)
# Exibir os gráficos lado a lado
col1, = st.columns(1)
col2, col3 = st.columns(2)
with col1:
    st.plotly_chart(fig_setores,use_container_width=True)
with col2:
    st.plotly_chart(fig_cargo, use_container_width=True)
    st.plotly_chart(fig_situacao, use_container_width=True)
with col3:
    st.plotly_chart(fig_funcao, use_container_width=True)
    st.plotly_chart(fig_quadro, use_container_width=True)