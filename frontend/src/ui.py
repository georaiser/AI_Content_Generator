import os
from dotenv import load_dotenv
import streamlit as st
from models.content_generation_models import ContentGeneration
from src.generate_content import compute_content


# Load environment variables from .env file
load_dotenv()

# Set the title of the Streamlit app
st.title("AI-Powered Reel Content Generator")

# Add a description for the app
st.write(
    """
    Ingresa una URL de un producto para crear el guion
"""
)

# Create input fields for URL, target audience, tone, and language
input_url = st.text_input("URL del producto", placeholder="https://www.falabella.com/")
new_target_audience = st.selectbox(
    "Público objetivo",
    options=["Adultos", "Niños", "Adolescentes", "Adultos mayores", "Familias"],
)
new_tone = st.selectbox(
    "Tono",
    options=["Informativo", "Divertido", "Serio", "Persuasivo"],
)
language = st.selectbox(
    "Idioma", options=["Español", "Inglés"]
)

print(language)

st.sidebar.header("Content Generator")
st.sidebar.table(
    {
        "URL del producto": input_url if input_url else "No ingresada",
        "Público objetivo": new_target_audience if new_target_audience else "No seleccionado",
        "Tono": new_tone if new_tone else "No seleccionado",
        "Idioma": language if language else "No seleccionado",
    }
)

# Create a button to generate content
if st.button("Generar contenido"):
    if input_url and new_target_audience and new_tone and language:
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8004/content_generator")
        # Create a payload using the ContentGeneration model
        payload = ContentGeneration(
            url=input_url,
            new_target_audience=new_target_audience,
            new_tone=new_tone,
            language=language
        )
        
        # Call the compute_content function to generate the script
        refined_script = compute_content(payload, backend_url)

        # Display the generated script and add a download button
        st.header("Guion Finalizado")
        if "error" in refined_script:
            st.error(refined_script["error"])
        else:
            st.text_area("Script", refined_script["script"], height=300)
            
        import json
        st.download_button(
            label="Descargar Guion en JSON",
            data=json.dumps(refined_script, ensure_ascii=False, indent=4),
            file_name="guion.json",
            mime="application/json"
        )
    else:
        # Show a warning if any input field is missing
        st.warning("Por favor, completa todos los campos.")

# Add a footer with the app's version
st.markdown(
    """
    ---
    **Versión 1.0**
    """
)

