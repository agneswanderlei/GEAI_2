import streamlit as st
import os
import sqlite3
import streamlit_authenticator as stauth

# ---Configuração Página---
st.set_page_config(layout='centered')
# ---Funções----
def adicionar_usuario(nome, username, perfil,senha_hash):
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Usuarios (nome, username, perfil, password)
            VALUES (?, ?, ?, ?)
            """,
            (nome, username, perfil, senha_hash)
        )
        conn.commit()
        st.success(f"✅ Usuário {username} adicionado com sucesso!")
    except sqlite3.IntegrityError:
        st.error("🚫 Esse nome de usuário já existe. Tente outro.")
    except Exception as e:
        st.error(f"❌ Erro ao adicionar usuário: {e}")
    finally:
        conn.close()

def consulta_user():
    conn = sqlite3.connect(os.path.join('db','Geai.db'))
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT * FROM Usuarios
        """
    )
    dados = cursor.fetchall()
    return dados

users_db = consulta_user()
if len(users_db) == 0:
    adicionar_usuario(nome='Admin', username='admin', password=stauth.Hasher.hash('1012ar1987'), perfil='admin')
    users_db =consulta_user()
credenciais = {
    "usernames": {
        usuario[2]: {
            "name": usuario[1],
            "password": usuario[3],
            "perfil": usuario[4]
        } for usuario in users_db
    }
}
authenticator = stauth.Authenticate(credentials=credenciais,cookie_name='Sage', cookie_key='Sage_key', cookie_expiry_days=1)

st.markdown("""
    <div style='margin-top: -50px; text-align: center;'>
        <h1>Controle de GEAI</h1>
    </div>

""", unsafe_allow_html=True)
pages = {
    'Agentes': [
        os.path.join('paginas','cadastro','Home_Agentes.py'),
        os.path.join('paginas','cadastro','Adicionar_Agentes.py'),
        os.path.join('paginas','cadastro','Editar_Agentes.py'),
        os.path.join('paginas','cadastro','Excluir_Agentes.py'),
        os.path.join('paginas','cadastro','Visualizar_Agentes.py'),

    ],
    'Vagas': [
        os.path.join('paginas','Vagas','Home_Vagas.py'),
        os.path.join('paginas','Vagas','Adicionar_Vagas.py'),
        os.path.join('paginas','Vagas','Editar_Vagas.py'),
        os.path.join('paginas','Vagas','Excluir_Vagas.py'),
        os.path.join('paginas','Vagas','Visualizar_Vagas.py'),

    ],
    'Pautas': [
        os.path.join('paginas','Pautas','Home_Pautas.py'),
        os.path.join('paginas','Pautas','Adicionar_Pautas.py'),
        os.path.join('paginas','Pautas','Editar_Pautas.py'),
        os.path.join('paginas','Pautas','Excluir_Pautas.py'),
        os.path.join('paginas','Pautas','Visualizar_Pautas.py'),

    ],
    'Gráficos': [
        os.path.join('paginas','Graficos','Graficos_Agentes.py'),
        # os.path.join('paginas','Graficos','Graficos_2.py'),
        # os.path.join('paginas','Graficos','Relatorio_1.py'),
        # os.path.join('paginas','Graficos','Relatorio_2.py')
    ],
    'Usuários': [
        os.path.join('paginas','Usuarios','Home_Usuarios.py'),
        os.path.join('paginas','Usuarios','Adicionar_Usuarios.py'),
        os.path.join('paginas','Usuarios','Editar_Perfil.py'),
        os.path.join('paginas','Usuarios','Editar_Senha.py'),
        os.path.join('paginas','Usuarios','Excluir_Usuarios.py'),

    ]
}

try:
    authenticator.login(captcha=False, max_login_attempts=2)

except stauth.exceptions.LoginError as e:
    if "Captcha entered incorrectly" in str(e):
        st.toast("❌ Captcha incorreto. Tente novamente.")
    else:
        st.toast(f"⚠️ {str(e)}")

if st.session_state.get('authentication_status'):
    perfil_usuario = credenciais['usernames'][st.session_state['username']]['perfil']
    if perfil_usuario == 'admin':
        pg = st.navigation(pages, position='sidebar', expanded=True)
        pg.run()
    else:
        pages = {
            'Agentes': [
                os.path.join('paginas','cadastro','Home_Agentes.py'),
                os.path.join('paginas','cadastro','Adicionar_Agentes.py'),
                os.path.join('paginas','cadastro','Editar_Agentes.py'),
                os.path.join('paginas','cadastro','Excluir_Agentes.py'),
                os.path.join('paginas','cadastro','Visualizar_Agentes.py'),

            ],
            'Vagas': [
                os.path.join('paginas','Vagas','Home_Vagas.py'),
                os.path.join('paginas','Vagas','Adicionar_Vagas.py'),
                os.path.join('paginas','Vagas','Editar_Vagas.py'),
                os.path.join('paginas','Vagas','Excluir_Vagas.py'),
                os.path.join('paginas','Vagas','Visualizar_Vagas.py'),

            ],
            'Pautas': [
                os.path.join('paginas','Pautas','Home_Pautas.py'),
                os.path.join('paginas','Pautas','Adicionar_Pautas.py'),
                os.path.join('paginas','Pautas','Editar_Pautas.py'),
                os.path.join('paginas','Pautas','Excluir_Pautas.py'),
                os.path.join('paginas','Pautas','Visualizar_Pautas.py'),

            ],
            'Gráficos': [
                os.path.join('paginas','Graficos','Graficos_Agentes.py'),
                # os.path.join('paginas','Graficos','Graficos_2.py'),
                # os.path.join('paginas','Graficos','Relatorio_1.py'),
                # os.path.join('paginas','Graficos','Relatorio_2.py')
            ],
            'Usuários': [
                # os.path.join('paginas','Usuarios','Adicionar_Usuarios.py'),
                # os.path.join('paginas','Usuarios','Editar_Perfil.py'),
                os.path.join('paginas','Usuarios','Editar_Senha.py'),
                # os.path.join('paginas','Usuarios','Excluir_Usuarios.py'),

            ]
        }
        pg = st.navigation(pages, position='sidebar', expanded=True)
        pg.run()
    authenticator.logout('Sair',location='sidebar', use_container_width=False)
elif st.session_state.get('authentication_status') is False:
    st.toast("🚫 Login inválido. Verifique suas credenciais.")
    
elif st.session_state.get('authentication_status') is None:
    st.toast("📝 Os campos devem ser preenchidos antes de continuar.")
    

# pg = st.navigation(pages, position='top',expanded=True)
# pg.run()
