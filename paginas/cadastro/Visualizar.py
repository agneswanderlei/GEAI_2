import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd

# definição de vagas
vagas_oficiais = 52
oficiais_cadastrados = 0
vagas_oficiais_preenchidas = 0
vagas_pracas = 352
pracas_cadastrados = 0
vagas_pracas_preenchidas = 0

def buscar_agentes():
    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT matricula, nome, nome_guerra, cargo FROM Agentes")
    colunas = [desc[0] for desc in cursor.description] # nome das colunas
    policiais = cursor.fetchall()
    conn.close()
    dados = pd.DataFrame(policiais,columns=colunas)
    dados = dados.rename(columns={
        'matricula': 'Matricula',
        'nome': 'Nome',
        'nome_guerra': 'Nome de Guerra',
        'cargo': 'Cargo'
    })
    return dados

# consulta dados daas vagas na tabela
cursor = sqlite3.connect('./db/Geai.db').cursor()
cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN') AND situacao NOT IN ('DESCREDENCIADO')")
oficiais_cadastrados = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN') AND situacao NOT IN ('DESCREDENCIADO')")
pracas_cadastrados = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE situacao_agente = 'EFETIVADO' AND cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
vagas_oficiais_preenchidas = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE situacao_agente = 'EFETIVADO' AND cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
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
st.dataframe(policiais, use_container_width=True)