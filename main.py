from .processors import (
    PDFToImageConverter, 
    GoogleVisionOCR, 
    QuestionSegmenter, 
    ImageCropper, 
    LocalStorageService, 
    QuestionExtractionPipeline
)

if __name__ == "__main__":
    pdf_converter = PDFToImageConverter(dpi=300)
    ocr_service = GoogleVisionOCR()
    segmenter = QuestionSegmenter()
    cropper = ImageCropper()
    storage = LocalStorageService(base_path="extracted_questions")

    pipeline = QuestionExtractionPipeline(pdf_converter, ocr_service, segmenter, cropper, storage)
    pipeline.run("exam_paper.pdf")