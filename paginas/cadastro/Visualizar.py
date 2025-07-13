import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3

# definição de vagas
vagas_oficiais = 52
vagas_oficiais_preenchidas = 0
vagas_pracas = 352
vagas_pracas_preenchidas = 0

# consulta dados daas vagas na tabela
cursor = sqlite3.connect('./db/Geai.db').cursor()
cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
vagas_oficiais_preenchidas = cursor.fetchall()[0][0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '1º TEN', '2º TEN')")
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
st.header('Visualizar Agentes Cadastrados.')
# Layout cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    card('Vagas Oficias', vagas_oficiais,'#0d6efd')
with col2:
    card('Vagas Preenchidas', vagas_oficiais_preenchidas,'#198754')
with col3:
    card('Vagas Praças', vagas_pracas,'#ffc107')
with col4:
    card('Vagas Preenchidas', vagas_pracas_preenchidas,'#dc3545')

st.markdown('<hr></hr>',unsafe_allow_html=True)