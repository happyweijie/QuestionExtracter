from processors import (
    PDFToImageConverter, 
    GoogleVisionOCR, 
    QuestionSegmenter, 
    ImageCropper, 
    LocalStorageService, 
    QuestionExtractionPipeline
)

if __name__ == "__main__":
    pdf_converter = PDFToImageConverter(dpi=300)
    print("PDF to Image Converter initialized.")
    ocr_service = GoogleVisionOCR()
    print("Google Vision OCR initialized.")
    segmenter = QuestionSegmenter()
    print("Question Segmenter initialized.")
    cropper = ImageCropper()
    print("Image Cropper initialized.") 
    storage = LocalStorageService(base_path="extracted_questions")

    pipeline = QuestionExtractionPipeline(pdf_converter, ocr_service, segmenter, cropper, storage)
    pipeline.run("exam_paper.pdf")

    print("Question extraction pipeline completed.")