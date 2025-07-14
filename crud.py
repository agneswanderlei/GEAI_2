import streamlit as st
import sqlite3

# Função para iniciar o banco de dados com os campos atualizados
def init_db():
    conn = sqlite3.connect('policiais.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS policiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE,
            nome TEXT,
            nome_guerra TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_policial(matricula, nome, nome_guerra):
    conn = sqlite3.connect('policiais.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO policiais (matricula, nome, nome_guerra) VALUES (?, ?, ?)', (matricula, nome, nome_guerra))
    conn.commit()
    conn.close()

def listar_policiais():
    conn = sqlite3.connect('policiais.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM policiais')
    data = cursor.fetchall()
    conn.close()
    return data

def atualizar_policial(id, matricula, nome, nome_guerra):
    conn = sqlite3.connect('policiais.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE policiais SET matricula=?, nome=?, nome_guerra=? WHERE id=?', (matricula, nome, nome_guerra, id))
    conn.commit()
    conn.close()

def deletar_policial(id):
    conn = sqlite3.connect('policiais.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM policiais WHERE id=?', (id,))
    conn.commit()
    conn.close()

init_db()

# Menu na Sidebar
st.sidebar.title("🚓 Controle de Policiais")
opcao = st.sidebar.radio("Escolha uma ação", ['Adicionar', 'Visualizar', 'Editar', 'Deletar'])

if opcao == 'Adicionar':
    st.subheader("➕ Adicionar Policial")
    matricula = st.text_input("Matrícula")
    nome = st.text_input("Nome completo")
    nome_guerra = st.text_input("Nome de guerra")
    if st.button("Salvar"):
        adicionar_policial(matricula, nome, nome_guerra)
        st.success(f"Policial {nome} cadastrado!")

elif opcao == 'Visualizar':
    st.subheader("📋 Lista de Policiais")
    lista = listar_policiais()
    st.table(lista)

elif opcao == 'Editar':
    st.subheader("✏️ Editar Policial")
    policiais = listar_policiais()
    ids = [p[0] for p in policiais]
    id_selecionado = st.selectbox("ID do Policial", ids)
    policial = next(p for p in policiais if p[0] == id_selecionado)

    matricula = st.text_input("Matrícula", policial[1])
    nome = st.text_input("Nome completo", policial[2])
    nome_guerra = st.text_input("Nome de guerra", policial[3])

    if st.button("Atualizar"):
        atualizar_policial(id_selecionado, matricula, nome, nome_guerra)
        st.success("Dados atualizados!")

elif opcao == 'Deletar':
    st.subheader("🗑️ Deletar Policial")
    lista = listar_policiais()
    ids = [p[0] for p in lista]
    id_selecionado = st.selectbox("ID para deletar", ids)

    if st.button("Excluir"):
        deletar_policial(id_selecionado)
        st.success("Policial removido com sucesso!")