from typing import List, Tuple
from PIL import Image

class ImageCropper:
    def crop(self, page_image: Image.Image, vertices_list: List[Tuple[int, int]]) -> Image.Image:
        xs = [v[0] for v in vertices_list]
        ys = [v[1] for v in vertices_list]
        bbox = (min(xs), min(ys), max(xs), max(ys))
        return page_image.crop(bbox)
    