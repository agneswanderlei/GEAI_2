import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import sqlite3
import pandas as pd
import io
st.set_page_config('Início',layout='centered')

# Funções
def listar_usuarios():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios')
    data = cursor.fetchall()
    conn.close()
    return data
usuarios = listar_usuarios()
ids_usuarios = [p[2] for p in usuarios]
ids_usuarios_nome = [p[1] for p in usuarios]



def buscar_dados():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT * FROM Usuarios
        """
    )
    dados = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    df_usuarios = pd.DataFrame(dados,columns=colunas)
    return df_usuarios
df_usuarios = buscar_dados()


def pautas_por_situacao(situacoes):
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
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
st.subheader('Lista dos Usuários 📋')
col1, col2 = st.columns(2)
# col3, col4, col5 = st.columns(3)
with col1:
    usuario_nome = st.multiselect('Nome', ids_usuarios_nome)
with col2:
    usuario = st.multiselect('Usuário', ids_usuarios)
# with col2:
#     agentes = st.multiselect('Agentes', ids_agentes)
# with col3:
#     situacao = st.multiselect('Situacao', ['Cadastro', 'Desligamento'])
# with col4:
#     data_inicio = st.date_input('Data Inicial', format='DD/MM/YYYY',value=None)
# with col5:
#     data_final = st.date_input('Data Final', format='DD/MM/YYYY', value=None)

# FILTROS
if usuario_nome:
    df_usuarios = df_usuarios[df_usuarios['nome'].isin(usuario_nome)]
if usuario:
    df_usuarios = df_usuarios[df_usuarios['username'].isin(usuario)]


# EXPORTAR PARA EXCEL
# criar um buffer na memoria
output = io.BytesIO()
# salvar df filtrado como arquivo excel
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_usuarios[['nome', 'username', 'perfil']].to_excel(writer, index=False, sheet_name='Pautas')
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
df_usuarios = df_usuarios.rename(
    columns={
        'nome': 'Nome',
        'username': 'Usuário',
        'perfil': 'Perfil',
    }
)

# DATAFRAME
st.dataframe(df_usuarios[['Nome','Usuário', 'Perfil']])

