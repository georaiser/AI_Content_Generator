# %%
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# %%
# %%
VISION_MODEL_NAME="llama-3.2-11b-vision-preview"

# %%
TEMPLATE="""
Eres un experto storyteller
en particular 
{topic}

El formato de salida debe ser el siguiente:{format_instructions}
"""

# %%
class ContentGenerationScript(BaseModel):
    text: str = Field(..., description="Contenido textual de la historia")

parser= JsonOutputParser(pydantic_object=ContentGenerationScript)

# %%
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key="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"
)


prompt = PromptTemplate(
    input_variables=["topic"],
    template=TEMPLATE,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


chain = LLMChain(llm=llm, prompt=prompt)


result = chain.invoke({"topic": "Ironman"})


result

# %%
import base64
from io import BytesIO
from PIL import Image
import os

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def describe_image(image_path):
    
    VISION_MODEL_NAME="llama-3.2-11b-vision-preview"
    client = Groq(api_key='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')
    vision_model = VISION_MODEL_NAME
    
    image = Image.open(image_path)
    base64_image = encode_image(image)
    
    completion = client.chat.completions.create(
        model=vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe la imagen a detalle en espanol"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
    )
    
    return completion.choices[0].message.content




# %%
image_path = "C:/Users/jcama/Desktop/rolex.jpg" 
description = describe_image(image_path)
print("Image description:", description)

# %%


# %%



