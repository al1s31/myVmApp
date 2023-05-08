from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os
from PIL import Image, ImageDraw, ImageFont

subscription_key = "0490cb2781614ddfb6287a917e8857bc"
endpoint = "https://ali-computervis.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

folder = "/Users/berataliseydi/Desktop/myVmApp/Images"
out_folder = "/Users/berataliseydi/Desktop/myVmApp/Outputs"
text_font= ImageFont.truetype("Arial.ttf", 16)
files = os.listdir(folder)

for file in files:
    file_path = os.path.join(folder, file)
    image = Image.open(file_path)

    image_draw = ImageDraw.Draw(image)
    with open(file_path, mode = 'rb') as image_stream :

        results = computervision_client.detect_objects_in_stream(image_stream)

        for object in results.objects:
            
            # Object property
            # Object size and position (h,w,x,y)
            # Object confidence

            left = object.rectangle.x
            top = object.rectangle.y
            height = object.rectangle.h
            width = object.rectangle.w

            box = [(left,top), (left + width, top + height)]
            image_draw.rectangle(box, outline = 'red', width=5)
            text = f'{object.object_property}({object.confidence * 100}%)'
            image_draw.text((left + 5 - 1, top + height - 30 + 1),text, (0, 0, 0), font= text_font)
            image_draw.text((left + 5, top + height - 30),text, (255, 0, 0), font= text_font)

        image.save(os.path.join(out_folder, file))