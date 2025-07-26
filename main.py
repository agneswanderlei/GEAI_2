import streamlit as st
import os
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
        os.path.join('paginas','Graficos','Graficos_2.py'),
        os.path.join('paginas','Graficos','Relatorio_1.py'),
        os.path.join('paginas','Graficos','Relatorio_2.py')
    ]
}

pg = st.navigation(pages, position='top',expanded=True)
pg.run()
