import requests
from models.content_generation_models import ContentGeneration
import streamlit as st

def compute_content(payload: ContentGeneration, server_url: str):
    try:
        # Send a POST request to the server with the payload
        r = requests.post(
                server_url,
                json=payload.model_dump(),  # Convert the Pydantic model to a dictionary
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
        
        # Raise an exception if the request fails
        r.raise_for_status()
        
        # Extract and return the generated content from the response
        generated_content = r.json()
        
        return {
            "url": payload.url,
            "audience": payload.new_target_audience,
            "tone": payload.new_tone,
            "language": payload.language,
            "script": generated_content.get("generated_content", "No content generated")
        }
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions and return an error message
        return {
            "error": f"Request failed: {str(e)}",
            "url": payload.url,
            "audience": payload.new_target_audience,
            "tone": payload.new_tone,
            "language": payload.language,
            "script": "Failed to generate content"
        }