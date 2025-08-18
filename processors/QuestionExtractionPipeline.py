from .PDFToImageConverter import PDFToImageConverter
from .OCRService import OCRService
from .QuestionSegmenter import QuestionSegmenter
from .ImageCropper import ImageCropper
from .StorageService import StorageService

class QuestionExtractionPipeline:
    def __init__(
        self,
        pdf_converter: PDFToImageConverter,
        ocr_service: OCRService,
        segmenter: QuestionSegmenter,
        cropper: ImageCropper,
        storage: StorageService
    ):
        self.pdf_converter = pdf_converter
        self.ocr_service = ocr_service
        self.segmenter = segmenter
        self.cropper = cropper
        self.storage = storage

    def run(self, pdf_path: str):
        pages = self.pdf_converter.convert(pdf_path)

        for page_num, page_image in enumerate(pages, start=1):
            # Step 1: OCR the page
            ocr_results = self.ocr_service.extract_text_and_boxes(page_image)
            
            # Step 2: Segment questions into hierarchical structure
            questions_hierarchy = self.segmenter.segment(ocr_results)

            # Step 3: Process each main question
            for main_q_num, subparts in questions_hierarchy.items():
                for part_key, content in subparts.items():
                    # Determine if content is text or nested roman subparts
                    if isinstance(content, str):
                        blocks = [block for block in ocr_results if content in block["text"]]
                        if not blocks:
                            continue
                        all_vertices = [v for block in blocks for v in block["vertices"]]
                        cropped_img = self.cropper.crop(page_image, all_vertices)
                        self.storage.save(
                            cropped_img,
                            {"filename": f"page{page_num}_q{main_q_num}_{part_key}.png"}
                        )
                    elif isinstance(content, dict):  # nested roman numerals
                        for roman_key, roman_text in content.items():
                            blocks = [block for block in ocr_results if roman_text in block["text"]]
                            if not blocks:
                                continue
                            all_vertices = [v for block in blocks for v in block["vertices"]]
                            cropped_img = self.cropper.crop(page_image, all_vertices)
                            self.storage.save(
                                cropped_img,
                                {"filename": f"page{page_num}_q{main_q_num}_{part_key}_{roman_key}.png"}
                            )

