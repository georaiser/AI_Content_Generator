from fastapi import FastAPI, HTTPException
import logging
from src.content_generator import ContentGenerator
from models.content_generation_models import ContentGeneration
from src.scraping import FalabellaScraper

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Text Generation with LLMs",
    description="""Create high-quality text content using advanced Large Language Models (LLMs).  
                  Generate textual descriptions, narratives, and insights from images and text inputs.  
                  Access the Streamlit interface at port 8501 for an interactive experience.""",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    """Endpoint to check the health of the API"""
    return {"status": "ok"}

@app.post("/content_generator")   # Endpoint to generate content called in frontend by ui.py
def generate_content(request: ContentGeneration):
    """Generate content based on metadata scraped from the given URL"""
    try:
        # Log the start of the scraping process
        logger.info(f"Scraping metadata from URL: {request.url}")

        # Scrape metadata using FalabellaScraper
        scraper = FalabellaScraper()
        metadata = scraper.scrape(request.url)
        encoded_image = metadata["encode_concatenated_image"] 

        # Validate if metadata is valid
        if not metadata or not isinstance(metadata, dict):
            raise ValueError("No se pudo extraer metadata válida del producto.")

        # Log the scraped metadata
        # logger.info(f"Metadata scraped: {metadata}")

        # Generate content using the ContentGenerator
        generator = ContentGenerator()
        content = generator.generate_content(
            metadata=metadata,
            target_audience=request.target_audience,
            tone=request.tone,
            language=request.language,
        )
        # Log successful content generation
        logger.info("Content generated successfully")
        generated_content = {"generated_content": content}
        return generated_content, encoded_image

    except ValueError as ve:
        # Handle ValueError and log the error
        logger.error(f"ValueError: {ve}")
        raise HTTPException(
            status_code=400, detail={"error": "Datos inválidos", "message": str(ve)}
        )

    except Exception as e:
        # Handle unexpected errors and log the error
        logger.error(f"Error interno: {e}")
        raise HTTPException(
            status_code=500, detail={"error": "Error interno", "message": str(e)}
        )