# dalle_processing/dalle_handler.py

import os
import openai

def generate_image_from_text(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )

    if response and response.get('data') and len(response['data']) > 0:
        return response['data'][0]['url']
    else:
        return None