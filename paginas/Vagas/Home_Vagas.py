import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
import io
st.set_page_config('Início',layout='centered')

# definição de options
options_status = [
    '🟢 Vagas disponíveis',
    '❌ Vagas excedidas',
    '✅ Vagas completas'
]
def listar_setores():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Vagas')
    data = cursor.fetchall()
    conn.close()
    return data
setores = listar_setores()
ids = [s[0] for s in setores]

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
tabela_final = tabela_final.rename(
    columns={
        'setor': 'Setor',
        'vagas': 'Vagas',
        'preenchidas': 'Preenchidas'
    }
)


st.subheader('Resumo de Vagas por Setor 📋')
col1, col2 = st.columns(2)
with col1:
    setor = st.multiselect('Setor', ids)
with col2:
    status = st.multiselect('Status', options_status)



# EXPORTAR PARA EXCEL
# criar um buffer na memoria
output = io.BytesIO()
# salvar df filtrado como arquivo excel
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    tabela_final[['Setor', 'Vagas', 'Preenchidas']].to_excel(writer, index=False, sheet_name='Setores')
# retorna ao inicio do buffer
output.seek(0)
st.download_button(
    "📤 Baixar Excel",
    data = output,
    file_name='Setores_Preenchidos.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
st.markdown(
    '<hr></hr>',unsafe_allow_html=True
)
# ESTILIZANDO TABELA
tabela_final['Status'] = tabela_final.apply(
    lambda row: (
        '❌ Vagas excedidas' if row['Preenchidas'] > row['Vagas'] else '✅ Vagas completas' if row['Preenchidas'] == row['Vagas'] else '🟢 Vagas disponíveis'
    ),axis=1
)



# 🎨 Função para destacar a célula "Setor" com base nas regras
def destacar_setor(row):
    estilo = []
    for col in row.index:
        if col == 'Setor':
            if row['Preenchidas'] > row['Vagas']:
                estilo.append('background-color: #8b0000; color: white;')  # vermelho p/ excedidas
            elif row['Preenchidas'] == row['Vagas']:
                estilo.append('background-color: #F28500; color: white;')  # vermelho escuro p/ completas
            else:
                estilo.append('')  # sem cor p/ disponíveis
        else:
            estilo.append('')
    return estilo

# FILTROS
if setor:
    tabela_final = tabela_final[tabela_final['Status'].isin(setor)]
if status:
    tabela_final = tabela_final[tabela_final['Status'].isin(status)]

# 🧠 Aplica o estilo por linha
dados_resumidos = tabela_final[['Setor', 'Vagas', 'Preenchidas', 'Status']]
styled_df = dados_resumidos.style.apply(destacar_setor, axis=1)

st.dataframe(styled_df, use_container_width=True)
