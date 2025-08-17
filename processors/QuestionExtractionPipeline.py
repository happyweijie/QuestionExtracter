from .PDFToImageConverter import PDFToImageConverter
from .OCRService import OCRService
from .QuestionSegmenter import QuestionSegmenter
from .ImageCropper import ImageCropper
from .StorageService import StorageService

class QuestionExtractionPipeline:
    def __init__(self, pdf_converter: PDFToImageConverter, ocr_service: OCRService,
                 segmenter: QuestionSegmenter, cropper: ImageCropper, storage: StorageService):
        self.pdf_converter = pdf_converter
        self.ocr_service = ocr_service
        self.segmenter = segmenter
        self.cropper = cropper
        self.storage = storage

    def run(self, pdf_path: str):
        pages = self.pdf_converter.convert(pdf_path)

        for page_num, page_image in enumerate(pages, start=1):
            ocr_results = self.ocr_service.extract_text_and_boxes(page_image)
            questions = self.segmenter.segment(ocr_results)

            for q_idx, q_blocks in enumerate(questions, start=1):
                all_vertices = [v for block in q_blocks for v in block["vertices"]]
                cropped_img = self.cropper.crop(page_image, all_vertices)
                self.storage.save(
                    cropped_img,
                    {"filename": f"page{page_num}_q{q_idx}.png"}
                )
