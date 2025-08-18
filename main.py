from processors import (
    PDFToImageConverter,
    GoogleVisionOCR,
    QuestionSegmenter,
    ImageCropper,
    LocalStorageService,
    QuestionExtractionPipeline
)

def main(pdf_path: str, output_dir: str):
    # Initialize components
    pdf_converter = PDFToImageConverter(dpi=300)
    print("[INFO] PDF to Image Converter initialized.")
    
    ocr_service = GoogleVisionOCR()
    print("[INFO] Google Vision OCR initialized.")
    
    segmenter = QuestionSegmenter()
    print("[INFO] Question Segmenter initialized.")
    
    cropper = ImageCropper()
    print("[INFO] Image Cropper initialized.")
    
    storage = LocalStorageService(base_path=output_dir)
    print(f"[INFO] Local Storage Service initialized at '{output_dir}'.")

    # Create and run pipeline
    pipeline = QuestionExtractionPipeline(
        pdf_converter, ocr_service, segmenter, cropper, storage
    )
    pipeline.run(pdf_path)

    print("[INFO] Question extraction pipeline completed.")

if __name__ == "__main__":
    main(pdf_path="tut01.pdf", output_dir="extracted_questions")
