from pydantic import BaseModel

class ContentGeneration(BaseModel):
    url: str
    target_audience: str
    tone: str
    language: str