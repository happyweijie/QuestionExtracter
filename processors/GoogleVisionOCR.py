import io
from PIL import Image
from google.cloud import vision
from .OCRService import OCRService

class GoogleVisionOCR(OCRService):
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def extract_text_and_boxes(self, image: Image.Image):
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        content = img_byte_arr.getvalue()

        gcv_image = vision.Image(content=content)
        response = self.client.document_text_detection(image=gcv_image)

        results = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                vertices = [(v.x, v.y) for v in block.bounding_box.vertices]
                text = "\n".join([word.symbols[0].text for para in block.paragraphs for word in para.words])
                results.append({"text": text, "vertices": vertices})
        return results