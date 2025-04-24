# -*- coding: utf-8 -*-
import base64
from PIL import Image
from io import BytesIO

class DisplayImage:
    @staticmethod
    def display_image(imagen_encoded):
        if imagen_encoded:
            # Decode the base64 image
            image_data = base64.b64decode(imagen_encoded)
            # Decode the image data
            return Image.open(BytesIO(image_data))
        else:
            print("No hay imagen para mostrar.")


