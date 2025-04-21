from pydantic import BaseModel, Field

class ContentGenerationScript(BaseModel):
    content: str = Field(..., description="Contenido textual del reel")

# Define the ToneGenerationScript class with a field for the refined content
class ToneGenerationScript(BaseModel):
    content: str = Field(..., description="Contenido refinado con tono específico")

# Define the ContentGeneration class with fields for URL, target audience, tone, and language
class ContentGeneration(BaseModel):
    url: str
    target_audience: str = Field(..., description="Público objetivo para el contenido")
    tone: str = Field(..., description="Tono deseado para el contenido")
    language: str = Field(default="español", description="Idioma del contenido")
