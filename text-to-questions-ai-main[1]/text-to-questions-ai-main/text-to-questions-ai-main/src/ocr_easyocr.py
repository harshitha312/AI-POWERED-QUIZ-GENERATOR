import pytesseract
from PIL import Image

def extract_text_from_image(image: Image.Image) -> str:
    # Convert to grayscale for better OCR accuracy
    gray = image.convert('L')
    text = pytesseract.image_to_string(gray)
    return text.strip()
