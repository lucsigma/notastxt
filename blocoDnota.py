
import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

st.title("📓 Bloco de notas")

# Entrada de texto
texto = st.text_area("Digite suas anotações abaixo:", height=300)

# Inicializa estado
if "notas" not in st.session_state:
    st.session_state.notas = []

if "editando" not in st.session_state:
    st.session_state.editando = None

# Salvar nova nota
if st.button("Salvar Nota"):
    if texto.strip():
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.notas.append({"Data/Hora": data_hora, "Texto": texto})
        st.success("Nota salva com sucesso!")
    else:
        st.warning("Digite algo antes de salvar.")

# Mostrar notas
if st.session_state.notas:
    st.subheader("🗂 Suas Notas Salvas:")

    for idx, nota in enumerate(reversed(st.session_state.notas)):
        real_idx = len(st.session_state.notas) - 1 - idx  # índice real

        st.markdown(f"🕒 {nota['Data/Hora']}")

        # Se estiver em modo edição:
        if st.session_state.editando == real_idx:
            novo_texto = st.text_area("Editar nota:", value=nota["Texto"], key=f"edit_{real_idx}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Salvar Edição", key=f"save_{real_idx}"):
                    st.session_state.notas[real_idx]["Texto"] = novo_texto
                    st.session_state.editando = None
                    st.success("Nota editada com sucesso!")
                    st.rerun()

            with col2:
                if st.button("❌ Cancelar", key=f"cancel_{real_idx}"):
                    st.session_state.editando = None
                    st.rerun()
        else:
            st.text_area(
                label="",
                value=nota["Texto"],
                height=150,
                key=f"nota_{real_idx}",
                disabled=True
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏ Editar", key=f"editar_{real_idx}"):
                    st.session_state.editando = real_idx
                    st.rerun()
            with col2:
                if st.button("🗑 Excluir", key=f"excluir_{real_idx}"):
                    st.session_state.notas.pop(real_idx)
                    st.success("Nota excluída com sucesso!")
                    st.rerun()

# Gerar texto para download
if st.session_state.notas:
    txt_buffer = StringIO()
    for nota in st.session_state.notas:
        txt_buffer.write(f"{nota['Data/Hora']}:\n{nota['Texto']}\n\n")

    st.download_button(
        label="📥 Baixar Notas em .txt",
        data=txt_buffer.getvalue(),
        file_name="bloco_de_notas.txt",
        mime="text/plain"
    )