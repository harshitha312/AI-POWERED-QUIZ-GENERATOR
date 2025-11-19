import easyocr
import numpy as np

def extract_text_easyocr(img_path : str, use_gpu: bool = True):
    """
    Extract text from an image using EasyOCR.
    Args:
        image_path (str): Path to the image file.
        use_gpu (bool): Whether to use GPU for faster processing (default: True).
    Returns:
        str: Extracted text as a single string.
    """
    reader = easyocr.Reader(['en'], use_gpu) #Use GPU for faster processing
    result = reader.readtext(img_path, detail=0, paragraph=True)
    return ' '.join(result)
