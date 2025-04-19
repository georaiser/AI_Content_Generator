import os
import base64
import requests
import math
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from backend.src.llm import GroqModelHandler

# load .env
load_dotenv()

class ImageGridDescriber:
    def __init__(self):
        # TODO: Initialize the GroqModelHandler client and load the vision model name from environment variables
        self.client = GroqModelHandler().get_client()
        self.vision_model = os.getenv("VISION_MODEL_NAME")

    @staticmethod
    def encode_image(image: Image.Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def concatenate_images_square(self, urls, img_size=(200, 200)):
        # Download and resize images
        images = []
        for url in urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).resize(img_size)
            images.append(img)

        # Calculate grid size
        n = len(images)
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)    
 
        # Create a new blank image for the grid
        grid_width = cols * img_size[0]
        grid_height = rows * img_size[1]
        grid_img = Image.new('RGB', (grid_width, grid_height), color='white')
        
        # Place images in the grid
        for i, img in enumerate(images):
            if i >= rows * cols:
                break
                
            row = i // cols
            col = i % cols
            
            x = col * img_size[0]
            y = row * img_size[1]
            
            grid_img.paste(img, (x, y))

        # Save or show the final image
        grid_img.save("grid.jpg")
        #grid_img.show()
        
        return grid_img  # Returns a PIL Image object

    def get_image_description(self, concatenated_image):
        
        base64_image = self.encode_image(concatenated_image)
        
        prompt = "Describe el producto en la imagen"

        completion = self.client.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
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