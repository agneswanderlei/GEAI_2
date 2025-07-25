import streamlit as st
import sqlite3
import time

def criar_tabela_pautas():

    conn = sqlite3.connect('./db/Geai.db')
    cursor = conn.cursor()
    cursor.executescript(
        """
            CREATE TABLE IF NOT EXISTS Pautas (
            num_pauta INTEGER PRIMARY KEY,
            data_envio TEXT NOT NULL,
            observacao TEXT NOT NULL,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
            CREATE TABLE IF NOT EXISTS Agentes_pauta (
            id INTEGER PRIMARY KEY,
            num_pauta INTEGER,
            matricula INTEGER,
            situacao_agente TEXT NOT NULL,
            FOREIGN KEY (num_pauta) REFERENCES Pautas(num_pauta)
            FOREIGN KEY (matricula) REFERENCES Agentes(matricula)
        );
    """
    )
    conn.commit()
    conn.close()

def inserir_pautas(num_pauta, data_envio, observacao):
    try:

        conn = sqlite3.connect('./db/Geai.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Pautas(
                num_pauta,
                data_envio,
                observacao
            )
            VALUES (?, ?, ?)
        """,
        (num_pauta, data_envio, observacao)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error('Pauta já cadastrada')
    except Exception as e:
        st.error(f'❌ Não foi possível cadastrar Pauta {e}')
        return False
    finally:
        conn.commit()
        conn.close()

def inserir_agentes_pautas(num_pauta, matricula, situacao):
    try:
        conn = sqlite3.connect('./db/Geai.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Agentes_pauta(
                num_pauta,
                matricula,
                situacao_agente
            )
            VALUES (?, ?, ?)
        """,
        (num_pauta, matricula, situacao)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error('Erro ao adicionar agentes!')
    except Exception as e:
        st.error(f'❌ Não foi possível cadastrar agentes {e}')
        return False
    finally:
        conn.commit()
        conn.close()

def atualizar_pauta(num_pauta, nova_data_envio, nova_observacao):
    try:
        conn = sqlite3.connect('./db/Geai.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Pautas
            SET data_envio = ?, observacao = ?
            WHERE num_pauta = ?
            """,
            (nova_data_envio, nova_observacao, num_pauta)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f'❌ Erro ao atualizar pauta: {e}')
        return False
    finally:
        conn.close()

def atualizar_agentes_pauta(num_pauta, lista_agentes):
    try:
        conn = sqlite3.connect('./db/Geai.db')
        cursor = conn.cursor()

        # Remover os agentes atualizados
        cursor.execute(
            "DELETE FROM Agentes_pauta WHERE num_pauta = ?", (num_pauta,)
        )
        for agente, situacao in lista_agentes:
            matricula = int(agente.split(' - ')[0])
            cursor.execute(
                """
                INSERT INTO Agentes_pauta (
                    num_pauta,
                    matricula,
                    situacao_agente
                ) VALUES (?, ?, ?)
                """,
                (num_pauta, matricula, situacao)
            )
        conn.commit()
        return True
    except Exception as e:
        st.error(f'❌ Erro ao atualizar agentes da pauta: {e}')
        return False
    finally:
        conn.close()