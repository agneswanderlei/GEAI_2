import sqlite3
import pandas as pd


conn = sqlite3.connect('./db/Geai.db')
cursor = conn.cursor()
cursor.execute(
    """
    SELECT setor FROM Agentes
"""
)
colunas = [desc[0] for desc in cursor.description]
dados = cursor.fetchall()
# EXEMPLO DE COMO FAZER UM CONT.SE NO PANDAS
df = pd.DataFrame(dados,columns=colunas)
df.value_counts()['SS 2']
setor = df['setor'].value_counts()
setor['SS 1']
s2 = int((df['setor'] == 'SS1').sum())
s3 = int((df['setor'] == 'NIE').sum())
ss = s2 + s3

# EXEMPLO DE COMO VER QUANTAS VAGAS ESTÃO PREENCHIDAS POR SETOR:
cursor.execute(
    """
    SELECT setor, vagas FROM Vagas
"""
)
colunas = [desc[0] for desc in cursor.description]
dados = cursor.fetchall()
df_vagas = pd.DataFrame(dados,columns=colunas)

cursor.execute(
    """
        SELECT setor, COUNT(*) as v_prenchidas FROM Agentes
        WHERE situacao_agente = 'RECEBENDO GEAI'
        GROUP BY setor
    """
)
dados1 = cursor.fetchall()
conn.close()
df_contagem = pd.DataFrame(dados1,columns=['setor', 'v_prenchidas']) 
tabela_final = df_vagas.merge(df_contagem,on='setor',how='left')
tabela_final['v_prenchidas'] = tabela_final['v_prenchidas'].fillna(0).astype(int) # serve para retirar os campos em que estiver com NaN ou seja vazio e transforma em 0

