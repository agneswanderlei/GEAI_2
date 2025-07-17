import streamlit as st

st.title('Controle de GEAI',anchor=False,)
pages = {
    'Agentes': [
        'paginas\cadastro\Home.py',
        'paginas\cadastro\Adicionar.py',
        'paginas\cadastro\Editar.py',
        'paginas\cadastro\Excluir.py',
        'paginas\cadastro\Visualizar.py',

    ],
    'Relatórios': [
        'paginas\Relatorios\Graficos_1.py',
        'paginas\Relatorios\Graficos_2.py',
        'paginas\Relatorios\Relatorio_1.py',
        'paginas\Relatorios\Relatorio_2.py'
    ]
}

pg = st.navigation(pages, position='top',expanded=True)
pg.run()
