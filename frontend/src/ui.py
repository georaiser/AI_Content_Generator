import os
from dotenv import load_dotenv
import streamlit as st
import logging
import json
from models.content_generation_models import ContentGeneration
from src.generate_content import compute_content
from src.display_image import DisplayImage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Set the title of the Streamlit app
st.title("AI-Powered Reel Content Generator")
# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "URL Content"

def main_page():
    st.sidebar.title("Navigation")
    active_tab = st.sidebar.radio("Select Tab", ["URL Content", "Contact Us"])
    # Update active tab in session state
    st.session_state.active_tab = active_tab
    # Display different sidebar content based on active tab
    if st.session_state.active_tab == "URL Content":
        # Add a description for the app
        st.write(
            """Ingresa URL de producto para crear el guion""")
        # Create input fields for URL, target audience, tone, and language
        input_url = st.text_input("URL del producto", placeholder="https://www.falabella.com/")
        target_audience = st.selectbox(
            "Público objetivo",
            options=["Adultos", "Niños", "Adolescentes", "Adultos mayores", "Familias"],
        )
        tone = st.selectbox(
            "Tono",
            options=["Informativo", "Divertido", "Serio", "Persuasivo"],
        )
        language = st.selectbox(
            "Idioma", options=["Español", "Inglés"]
        )

        # Create a button to generate content
        if st.button("Generar contenido"):
            with st.spinner("Processing URL..."):
                st.sidebar.header("Content Generator")
                st.sidebar.table(
                    {
                        "URL del producto": input_url if input_url else "No ingresada",
                        "Público objetivo": target_audience if target_audience else "No seleccionado",
                        "Tono": tone if tone else "No seleccionado",
                        "Idioma": language if language else "No seleccionado",
                    }
                )
                if input_url and target_audience and tone and language:
                    backend_url = os.getenv("BACKEND_URL", "http://backend:8004/content_generator")
                    #backend_url = os.getenv("API_URL", "http://backend:8004/content_generator")  # Docker default

                    # Create a payload using the ContentGeneration model
                    payload = ContentGeneration(
                        url=input_url,
                        target_audience=target_audience,
                        tone=tone,
                        language=language
                    )

                    # Log the payload being sent to the backend
                    logger.info(f"Sending payload: {payload}")
                    
                    # Call the compute_content function to generate the script and get encoded image
                    refined_script, encoded_image = compute_content(payload, backend_url)

                    # Display the generated image
                    with st.sidebar:
                        image = DisplayImage().display_image(encoded_image)
                        st.image(image, caption="Generated Image 1")

                    # Display the generated script and add a download button
                    st.header("Guion Finalizado")
                    if "error" in refined_script:
                        st.error(refined_script["error"])
                    else:
                        st.text_area("Script", refined_script["script"], height=180)
                        
                    st.download_button(
                        label="Descargar Guion en JSON",
                        data=json.dumps(refined_script, ensure_ascii=False, indent=4),
                        file_name="guion.json",
                        mime="application/json"
                    )
                else:
                    # Show a warning if any input field is missing
                    st.warning("Por favor, completa todos los campos.")

    elif st.session_state.active_tab == "Contact Us":
        st.sidebar.markdown(
            """
            ### Contact Us
            - [LinkedIn](https://www.linkedin.com/in/jrodrigueze/) 
            - [GitHub](https://github.com/georaiser) 
            """)
        # Create a contact form
        st.header("Contáctanos")
        st.write(
            """
            Si tienes alguna pregunta o comentario, no dudes en contactarnos.
            """
        )
        name = st.text_input("Nombre")
        email = st.text_input("Correo electrónico")
        message = st.text_area("Mensaje")

        if st.button("Enviar"):
            if name and email and message:
                # Log the contact form submission
                logger.info(f"Contact form submitted by {name} ({email}): {message}")
                st.success("Gracias por tu mensaje. Nos pondremos en contacto contigo pronto.")
            else:
                st.warning("Por favor, completa todos los campos.")


# Run the app
if __name__ == "__main__":
    main_page()
    # Add a footer with the app's version
    st.markdown(
        """
        ---
        **Versión 1.0**
        """
    )

