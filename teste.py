import streamlit as st
import sqlite3

def get_connection():
    return sqlite3.connect("gratificacoes.db")

st.title("Controle de Ofícios e Policiais 👮📄")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Policial", "Cadastrar Ofício", "Vincular Policial ao Ofício", "Visualizar"])

# Cadastrar policial
if menu == "Cadastrar Policial":
    nome = st.text_input("Nome do policial")
    if st.button("Cadastrar"):
        conn = get_connection()
        conn.execute("INSERT INTO policiais (nome) VALUES (?)", (nome,))
        conn.commit()
        st.success("Policial cadastrado com sucesso!")
        conn.close()

# Cadastrar ofício
elif menu == "Cadastrar Ofício":
    numero = st.text_input("Número do ofício")
    data = st.date_input("Data do ofício")

    # Buscar policiais
    conn = get_connection()
    policiais = conn.execute("SELECT id, nome FROM policiais").fetchall()
    conn.close()

    # Seleção múltipla
    policiais_selecionados = st.multiselect(
        "Selecionar policiais para este ofício",
        policiais,
        format_func=lambda x: x[1]
    )

    if st.button("Cadastrar"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO oficios (numero, data) VALUES (?, ?)", (numero, str(data)))
        oficio_id = cursor.lastrowid

        for policial in policiais_selecionados:
            cursor.execute("INSERT INTO oficio_policiais (oficio_id, policial_id) VALUES (?, ?)", (oficio_id, policial[0]))

        conn.commit()
        conn.close()
        st.success("Ofício e vínculos cadastrados com sucesso! 🎉")
# Vincular policial ao ofício
elif menu == "Vincular Policial ao Ofício":
    conn = get_connection()
    policiais = conn.execute("SELECT id, nome FROM policiais").fetchall()
    oficios = conn.execute("SELECT id, numero FROM oficios").fetchall()
    conn.close()

    policial = st.selectbox("Selecionar policial", policiais, format_func=lambda x: x[1])
    oficio = st.selectbox("Selecionar ofício", oficios, format_func=lambda x: x[1])

    if st.button("Vincular"):
        conn = get_connection()
        conn.execute("INSERT INTO oficio_policiais (oficio_id, policial_id) VALUES (?, ?)", (oficio[0], policial[0]))
        conn.commit()
        st.success("Vínculo criado com sucesso!")
        conn.close()

# Visualizar vínculos
elif menu == "Visualizar":
    conn = get_connection()
    resultado = conn.execute("""
    SELECT o.numero, p.nome FROM oficio_policiais op
    JOIN oficios o ON o.id = op.oficio_id
    JOIN policiais p ON p.id = op.policial_id
    """).fetchall()
    conn.close()

    for numero, nome in resultado:
        st.write(f"📄 Ofício: {numero} — 👮 Policial: {nome}")