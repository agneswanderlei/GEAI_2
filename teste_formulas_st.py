import streamlit as st
import sqlite3
import pandas as pd

# Conectando ao banco
conn = sqlite3.connect("./db/Geai.db")
cursor = conn.cursor()

# Obter agentes do banco
cursor.execute("SELECT matricula, nome FROM Agentes")
dados_agentes = cursor.fetchall()
opcoes_agentes = [f"{matricula} - {nome}" for matricula, nome in dados_agentes]

# Inicializar estado
if 'agentes_pauta' not in st.session_state:
    st.session_state.agentes_pauta = []

# Formulário principal
st.title("Cadastrar Pauta")
col4, col5 = st.columns(2)
with col4:
    num_pauta = st.text_input("Número da pauta")
with col5:
    data_envio = st.date_input("Data de envio")

# Formulário de agentes da pauta
st.subheader("Adicionar agentes à pauta")
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    agente_selecionado = st.selectbox('Agente', opcoes_agentes)
with col2:
    situacao = st.selectbox("Situação", ["Cadastro", "Desligamento"])
with col3:
    if st.button('Acicionar'):
        st.session_state.agentes_pauta.append((agente_selecionado, situacao))
        print(st.session_state.agentes_pauta)

# Exibir agentes adicionados
observacao = st.text_area("Observação",height=200)

# Atualizar DataFrame com os agentes do session_state
df_agentes = pd.DataFrame(st.session_state.agentes_pauta, columns=["Agente", "Situação"])

# Editável
df_editado = st.data_editor(
    df_agentes,
    hide_index=True,
    disabled=["Agente", "Situação"],
    num_rows="dynamic",
    use_container_width=True
)

# Atualizar session_state com a versão editada
st.session_state.agentes_pauta = df_editado.to_records(index=False).tolist()

# Exibir lista com botões de remover
st.write("### 👮‍♂️ Agentes adicionados à pauta")
for i, (agente, situacao) in enumerate(st.session_state.agentes_pauta):
    col1, col2, col3 = st.columns([6, 3, 1])
    with col1:
        st.write(f"**{agente}**")
    with col2:
        st.write(situacao)
    with col3:
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.agentes_pauta.pop(i)
            st.rerun()
# Botão para salvar no banco
if st.button("Salvar pauta"):
    # Inserir pauta
    cursor.execute("INSERT INTO Pauta (num_pauta, data_envio, observacao) VALUES (?, ?, ?)", 
                   (num_pauta, str(data_envio), observacao))
    conn.commit()

    for agente, situacao in st.session_state.agentes_pauta:
        matricula = int(agente.split(" - ")[0])
        cursor.execute("INSERT INTO Agentes_pauta (num_pauta, matricula, situacao_agente) VALUES (?, ?, ?)",
                       (num_pauta, matricula, situacao))
    conn.commit()
    st.success("✅ Pauta e agentes cadastrados com sucesso!")
    st.session_state.agentes_pauta.clear()