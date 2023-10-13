import streamlit as st
from PIL import Image
from src import config


def sidebar():
    with st.sidebar:
        image = Image.open(config.LOGO)

        st.image(image, use_column_width=True)  # Adjust image to fit sidebar width
        st.markdown("## 📖 Como usar Policy Pro")
        st.markdown("1️⃣ Escribe tu pregunta en el cuadro de texto.")
        st.markdown("---")
        st.markdown("🔍 Acerca de")
        st.markdown(
            "🤖 Este es un demo de Policy Pro, un chatbot para pólizas de seguros."
        )
