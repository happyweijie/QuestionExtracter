import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pandas as pd
import re
import os

# --- CONFIGURATION (Update if needed) ---
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_questions_from_pdf_fixed(pdf_path, output_dir="extracted_questions_fixed"):
    """
    Extracts each question from a PDF file as a separate image using improved logic
    to keep multi-part questions together.

    Args:
        pdf_path (str): The path to the input PDF file.
        output_dir (str): The directory to save the cropped question images.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    print(f"Processing {len(doc)} pages in '{pdf_path}'...")

    question_counter = 0
    
    for page_num, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DATAFRAME)
        
        # Clean up OCR data: remove low-confidence detections and empty text boxes
        df = ocr_data[ocr_data.conf > 30].copy()
        df['text'] = df['text'].str.strip()
        df.dropna(subset=['text'], inplace=True)
        df = df[df.text != '']

        # Group words into lines to analyze line structure
        lines = df.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'].apply(lambda x: ' '.join(list(x))).tolist()
        line_dfs = [group for _, group in df.groupby(['page_num', 'block_num', 'par_num', 'line_num'])]

        question_bounds = []
        current_question_indices = []

        # --- WHAT'S CHANGED ---
        # The logic below is more robust. It groups lines together and only
        # starts a *new* question when a line begins with a primary question
        # number like "1.", "2.", etc.
        
        for i, line_text in enumerate(lines):
            # Regex to find a line starting with a number and a period (e.g., "1. ", "2. ")
            is_new_question_start = re.match(r'^\s*\d+\.\s+', line_text)
            
            if is_new_question_start:
                if current_question_indices: # If we were already tracking a question, save it
                    question_bounds.append(current_question_indices)
                current_question_indices = [i] # Start a new question
            elif current_question_indices: # If we are in a question, add this line to it
                current_question_indices.append(i)
        
        if current_question_indices: # Add the last question found on the page
            question_bounds.append(current_question_indices)
            
        print(f"Found {len(question_bounds)} questions on page {page_num + 1}.")

        for indices in question_bounds:
            # Combine the DataFrames for all lines in the current question
            question_df = pd.concat([line_dfs[i] for i in indices])
            
            # Calculate the overall bounding box for the entire question
            left = question_df['left'].min()
            top = question_df['top'].min()
            right = (question_df['left'] + question_df['width']).max()
            bottom = (question_df['top'] + question_df['height']).max()
            
            padding = 20 # Add a small margin for better visuals
            crop_box = (left - padding, top - padding, right + padding, bottom + padding)
            
            cropped_img = img.crop(crop_box)
            
            question_counter += 1
            output_path = os.path.join(output_dir, f"question_{question_counter}.png")
            cropped_img.save(output_path)
            print(f"Saved: '{output_path}'")

# --- HOW TO USE ---
# Replace 'tut01.pdf' with your file path.
extract_questions_from_pdf_fixed('tut2.pdf')