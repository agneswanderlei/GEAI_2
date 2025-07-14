import streamlit as st
from funcoes.funcoes_cadastro import buscar_dados, atualizar_agente

# Campo para digitar matrícula e botão de busca
st.subheader("🔍 Buscar Agente por Matrícula")
matricula_busca = st.text_input("Digite a matrícula")
buscar = st.button("Buscar")

dados_agente = None
if buscar and matricula_busca.strip() != "":
    dados_agente = buscar_dados(matricula_busca)
    if not dados_agente:
        st.error("Matrícula não encontrada.")

# Se dados foram encontrados, exibe formulário preenchido
if dados_agente:
    with st.form("Editar agente", clear_on_submit=True):
        st.text_input("Matrícula", value=dados_agente[0], disabled=True)  # campo travado
        nome = st.text_input("Nome", value=dados_agente[1])
        nome_guerra = st.text_input("Nome de Guerra", value=dados_agente[2])

        cargo = st.selectbox("Cargo", [
            '',
            'CEL',
            'TC',
            'MAJ',
            'CAP',
            '1º TEN',
            '2º TEN',
            'SUB TEN',
            '1º SGT',
            '2º SGT',
            '3º SGT',
            'CB',
            'SD',
        ], index=[
            '',
            'CEL',
            'TC',
            'MAJ',
            'CAP',
            '1º TEN',
            '2º TEN',
            'SUB TEN',
            '1º SGT',
            '2º SGT',
            '3º SGT',
            'CB',
            'SD',
        ].index(dados_agente[3]))
        quadro = st.selectbox("Quadro", [
            '',
            'QOPM',
            'QOAPM',
            'QPMG'
        ], index=[
            '',
            'QOPM',
            'QOAPM',
            'QPMG'
        ].index(dados_agente[4]))
        setor = st.selectbox("Setor", [
            '',
            'CHEFIA',
            'ADJUNTO',
            'SSA',
            'NTMB',
            'SS CSP',
            'SS PC',
            'NA',
            'NO',
            'PERMANÊNCIA',
            'TI',  
            'SS CCI',
            'SS CI',
            'CR I',
            'CR II',
            'CR III',
            'NIE',
            'ASI-7 / 1º BPM',
            'ASI-11 / 2º BPM',
            'ASI-19 / 3º BPM',
            'ASI-14 / 4º BPM',
            'ASI-26 / 5º BPM',
            'ASI-6 / 6º BPM',
            'ASI-24 / 7º BPM',
            'ASI-23 / 8º BPM',
            'ASI-18 / 9º BPM',
            'ASI-13 / 10º BPM',
            'ASI-5 / 11º BPM',
            'ASI-4 / 12º BPM',
            'ASI-2 / 13º BPM',
            'ASI-21 / 14º BPM',
            'ASI-1 / 16º BPM',
            'ASI-8 / 17º BPM',
            'ASI-10 / 18º BPM',
            'ASI-3 / 19º BPM',
            'ASI-9 / 20º BPM',
            'ASI-6 / 25º BPM',
            'ASI-8 / 26º BPM',
            'ASI-15 / 15º BPM',
            'ASI-12 / 21º BPM',
            'ASI-16 / 22º BPM',
            'ASI-17 / 24º BPM',
            'ASI-11 / 3ª CIPM',
            'ASI-12 / 5ª CIPM',
            'ASI-16 / 6ª CIPM',
            'ASI-15 / 8ª CIPM',
            'ASI-13 / 10ª CIPM',
            'ASI-20 / 23º BPM',
            'ASI-22 / 1ª CIPM',
            'ASI-25 / 2ª CIPM',
            'ASI-22 / 4ª CIPM',
            'ASI-25 / 7ª CIPM'
        ], index=[
            '',
            'CHEFIA',
            'ADJUNTO',
            'SSA',
            'NTMB',
            'SS CSP',
            'SS PC',
            'NA',
            'NO',
            'PERMANÊNCIA',
            'TI',  
            'SS CCI',
            'SS CI',
            'CR I',
            'CR II',
            'CR III',
            'NIE',
            'ASI-7 / 1º BPM',
            'ASI-11 / 2º BPM',
            'ASI-19 / 3º BPM',
            'ASI-14 / 4º BPM',
            'ASI-26 / 5º BPM',
            'ASI-6 / 6º BPM',
            'ASI-24 / 7º BPM',
            'ASI-23 / 8º BPM',
            'ASI-18 / 9º BPM',
            'ASI-13 / 10º BPM',
            'ASI-5 / 11º BPM',
            'ASI-4 / 12º BPM',
            'ASI-2 / 13º BPM',
            'ASI-21 / 14º BPM',
            'ASI-1 / 16º BPM',
            'ASI-8 / 17º BPM',
            'ASI-10 / 18º BPM',
            'ASI-3 / 19º BPM',
            'ASI-9 / 20º BPM',
            'ASI-6 / 25º BPM',
            'ASI-8 / 26º BPM',
            'ASI-15 / 15º BPM',
            'ASI-12 / 21º BPM',
            'ASI-16 / 22º BPM',
            'ASI-17 / 24º BPM',
            'ASI-11 / 3ª CIPM',
            'ASI-12 / 5ª CIPM',
            'ASI-16 / 6ª CIPM',
            'ASI-15 / 8ª CIPM',
            'ASI-13 / 10ª CIPM',
            'ASI-20 / 23º BPM',
            'ASI-22 / 1ª CIPM',
            'ASI-25 / 2ª CIPM',
            'ASI-22 / 4ª CIPM',
            'ASI-25 / 7ª CIPM'
        ].index(dados_agente[5]))
        funcao = st.selectbox("Função", [
            '',
            'ADJUNTO',
            'AG. DE BUSCA',
            'ANALISTA',
            'AUXÍLIAR ADM',
            'CHEFE', 
            'COORDENADOR',
            'GRADUADO',
            'MOTORISTA',
            'PERMANÊNCIA',
            'SECRETÁRIA'
        ], index=[
            '',
            'ADJUNTO',
            'AG. DE BUSCA',
            'ANALISTA',
            'AUXÍLIAR ADM',
            'CHEFE', 
            'COORDENADOR',
            'GRADUADO',
            'MOTORISTA',
            'PERMANÊNCIA',
            'SECRETÁRIA'
        ].index(dados_agente[6]))
        situacao = st.selectbox("Situação", ["ATIVO", "INATIVO"], index=["ATIVO", "INATIVO"].index(dados_agente[7]))
        disponibilidade = st.selectbox("Disponibilidade", ["DISPONÍVEL", "INDISPONÍVEL", "AGUARDANDO PUBLICAÇÃO"], index=["DISPONÍVEL", "INDISPONÍVEL", "AGUARDANDO PUBLICAÇÃO"].index(dados_agente[8]))
        codigo_agente = st.text_input("Código Agente", value=dados_agente[9])
        observacao = st.text_area("Observações", value=dados_agente[10])
        
        atualizar = st.form_submit_button("Atualizar")
        if atualizar:
            atualizar_agente(
                dados_agente[0],
                nome,
                nome_guerra,
                cargo,
                quadro,
                setor,
                funcao,
                situacao,
                disponibilidade,
                codigo_agente,
                observacao
            )
            st.success("✅ Agente atualizado com sucesso!")
            st.rerun()