from abc import ABC, abstractmethod
from PIL import Image

class OCRService(ABC):
    @abstractmethod
    def extract_text_and_boxes(self, image: Image.Image):
        pass