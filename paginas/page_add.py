import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes.funcoes_cadastro import inserir_agente
import time
import sqlite3

# definição de vagas
vagas_oficiais = 52
vagas_oficiais_preenchidas = 0
vagas_pracas = 352
vagas_pracas_preenchidas = 0

# consulta dados daas vagas na tabela
cursor = sqlite3.connect('./db/Geai.db').cursor()
cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo IN ('CEL', 'TC', 'MAJ', 'CAP', '2º TEN', '1º TEN)")
vagas_oficiais_preenchidas = cursor.fetchall[0]

cursor.execute("SELECT COUNT(*) FROM Agentes WHERE cargo NOT IN ('CEL', 'TC', 'MAJ', 'CAP', '2º TEN', '1º TEN)")
vagas_oficiais_preenchidas = cursor.fetchall[0]

