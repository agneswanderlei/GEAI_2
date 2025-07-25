import streamlit as st

st.markdown("""
    <div style='margin-top: -50px; text-align: center;'>
        <h1>Controle de GEAI</h1>
    </div>

""", unsafe_allow_html=True)
pages = {
    'Agentes': [
        'paginas\cadastro\Home_Agentes.py',
        'paginas\cadastro\Adicionar_Agentes.py',
        'paginas\cadastro\Editar_Agentes.py',
        'paginas\cadastro\Excluir_Agentes.py',
        'paginas\cadastro\Visualizar_Agentes.py',

    ],
    'Vagas': [
        'paginas\Vagas\Home_Vagas.py',
        "paginas\Vagas\Adicionar_Vagas.py",
        'paginas\Vagas\Editar_Vagas.py',
        'paginas\Vagas\Excluir_Vagas.py',
        'paginas\Vagas\Visualizar_Vagas.py',

    ],
    'Pautas': [
        'paginas\Pautas\Home_Pautas.py',
        "paginas\Pautas\Adicionar_Pautas.py",
        'paginas\Pautas\Editar_Pautas.py',
        'paginas\Pautas\Excluir_Pautas.py',
        'paginas\Pautas\Visualizar_Pautas.py',

    ],
    'Gráficos': [
        'paginas\Graficos\Graficos_Agentes.py',
        'paginas\Graficos\Graficos_2.py',
        'paginas\Graficos\Relatorio_1.py',
        'paginas\Graficos\Relatorio_2.py'
    ]
}

pg = st.navigation(pages, position='top',expanded=True)
pg.run()
