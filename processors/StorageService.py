from abc import ABC, abstractmethod
from PIL import Image

class StorageService(ABC):
    @abstractmethod
    def save(self, image: Image.Image, metadata: dict):
        pass