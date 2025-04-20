from pydantic import BaseModel, HttpUrl

class ContentGeneration(BaseModel):
    url: HttpUrl
    new_target_audience: str = "default_audience"
    new_tone: str = "default_tone"
    language: str = "default_language"