from typing import List
from pdf2image import convert_from_path
from PIL import Image

class PDFToImageConverter:
    def __init__(self, dpi=300):
        self.dpi = dpi

    def convert(self, pdf_path: str) -> List[Image.Image]:
        return convert_from_path(pdf_path, dpi=self.dpi)
