import os
from PIL import Image
from .StorageService import StorageService

class LocalStorageService(StorageService):
    def __init__(self, base_path="output"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, image: Image.Image, metadata: dict):
        filename = metadata.get("filename", "question.png")
        save_path = os.path.join(self.base_path, filename)
        image.save(save_path)
        # Optionally save metadata as JSON