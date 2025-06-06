import requests
from models.content_generation_models import ContentGeneration
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compute_content(payload: ContentGeneration, server_url: str):
    try:
        # Send a POST request to the server with the payload
        response = requests.post(
                server_url,
                json=payload.model_dump(),  # Convert the Pydantic model to a dictionary
                headers={"Content-Type": "application/json"},
                timeout=20,
            )
        
        # Log the response status code and content
        logger.info(f"Status code: {response.status_code}")

        # Raise an exception if the request fails
        response.raise_for_status()
        
        # Extract and return the generated content from the response
        generated_content, encoded_image = response.json()
        
        logger.info(f"encoded: {encoded_image}")
        return {
            "url": payload.url,
            "audience": payload.target_audience,
            "tone": payload.tone,
            "language": payload.language,
            "script": generated_content.get("generated_content", "No content generated")
        }, encoded_image
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions and return an error message
        return {
            "error": f"Request failed: {str(e)}",
            "url": payload.url,
            "audience": payload.target_audience,
            "tone": payload.tone,
            "language": payload.language,
            "script": "Failed to generate content"
        }