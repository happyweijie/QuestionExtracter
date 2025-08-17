from pdf2image import convert_from_path
import os

# Ensure output folder exists
os.makedirs("images", exist_ok=True)

# Convert PDF to image list (1 image per page)
images = convert_from_path("exam_paper.pdf", dpi=300)
print("Conversion done!")

# Save images
for i, img in enumerate(images):
    img.save(os.path.join("images", f"page_{i + 1}.jpg"), "JPEG")

