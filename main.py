import streamlit as st
st.title('Bem vindo ao Controle de GEAI')
pages = {
    'Cadastro': [
        'paginas\page_add.py',
        'paginas\page_editar.py',
        'paginas\page_visualizar.py',
        'paginas\page_excluir.py'
    ],
    'Relatórios': [
        'paginas\page_rel_1.py',
        'paginas\page_rel_2.py',
        'paginas\page_grafico_1.py',
        'paginas\page_graf_2.py'
    ]
}

pg = st.navigation(pages, position='top',expanded=True)
pg.run()