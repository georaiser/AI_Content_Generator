import os
from dotenv import load_dotenv
import streamlit as st
from models.content_generation_models import ContentGeneration
from src.generate_content import compute_content


# TODO: Load environment variables from .env file
load_dotenv()


# TODO: Set the title of the Streamlit app
st.title("AI-Powered Reel Content Generator")

# TODO: Add a description for the app
st.write(
    """
Ingresa una url de un producto para crear el guion
"""
)

# TODO: Create input fields for URL, target audience, tone, and language
input_url = None
new_target_audience = None
new_tone = None
language = None

############# PRACTICANDO ######################
# x = st.slider("Select a value")
# st.write(x, "squared is", x * x)
####
# with st.form("my_form"):
#     text = st.text_area(
#         "Enter text:",
#         "What are the three key pieces of advice for learning how to code?",
#     )
#     submitted = st.form_submit_button("Submit")
    # if not openai_api_key.startswith("sk-"):
    #     st.warning("Please enter your OpenAI API key!", icon="⚠")
    # if submitted and openai_api_key.startswith("sk-"):
    #     generate_response(text)

st.sidebar.header("Configuración")
st.sidebar.table(
    {
        "URL del producto": st.text_input(
            "Ingresa la URL del producto", placeholder="https://www.falabella.com.pe/"
        ),
        "Público objetivo": st.selectbox(
            "Selecciona el público objetivo",
            options=[
                "Adultos",
                "Niños",
                "Adolescentes",
                "Adultos mayores",
                "Familias",
            ],
        ),
        "Tono": st.selectbox(
            "Selecciona el tono",
            options=["Informativo", "Divertido", "Serio", "Persuasivo"],
        ),
        "Idioma": st.selectbox(
            "Selecciona el idioma", options=["Español", "Inglés"]
        ),
    }
)

st.container()

#################################################


# TODO: Add a button to trigger content generation
if st.button("Generar Guion"):
    if input_url and new_target_audience and new_tone and language:
        backend_url = os.getenv("BACKEND_URL", "http://backend:8004/content_generator")
        # TODO: Create a payload using the ContentGeneration model
        payload = ContentGeneration(
            url=None,
            new_target_audience=None,
            new_tone=None,
            language=None,
        )

        # TODO: Call the compute_content function to generate the script
        refined_script = None

        # TODO: Display the generated script and add a download button
        st.header("Guion Finalizado")
        st.download_button(
            label="Descargar Guion en JSON",
            data=None,
            file_name=None,
            mime=None,
        )
    else:
        # TODO: Show a warning if any input field is missing
        st.warning("Por favor, completa todos los campos.")
