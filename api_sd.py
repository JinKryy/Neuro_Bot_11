import os
import requests
import io
import base64
import random
import json
from PIL import Image, PngImagePlugin

def img2img(mes, src):

    api_url = f"http://127.0.0.1:7860/sdapi/v1/img2img"
    with open(src, 'rb') as file:
        image_data = file.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    payload = {
        "init_images": [encoded_image],
        "prompt": "",
        "negative_prompt": "",
        "steps": 20,
        "width": 800,
        "height": 800,
        "denoising_strength": 0.85,
        "mask_blur": 4,
        "sampler_name": "Euler a",
        "restore_faces": True,
        "cfg_scale": 7,
        "script_name": "txt2mask v0.1.1",
        "script_args": [
            '',
            '',
            100,
            60,
            False,
        ]
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        encoded_result = response_data["images"][0]
        result_data = base64.b64decode(encoded_result)
        output_path = f"files/{mes}/photos/photos_1.jpg"
        with open(output_path, 'wb') as file:
            file.write(result_data)
    else:
        print("Ошибка при выполнении запроса:", response.text)
        return None