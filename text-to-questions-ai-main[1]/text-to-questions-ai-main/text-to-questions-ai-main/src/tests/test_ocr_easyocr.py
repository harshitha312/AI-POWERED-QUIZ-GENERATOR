import unittest
import os
from src.ocr_easyocr import extract_text_easyocr


class TestOCREasyOCR(unittest.TestCase):
    """Simplified unit test for EasyOCR"""

    def test_valid_image(self):
        """Test OCR on a valid printed or handwritten image."""
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../images/sample_image.png')
        text = extract_text_easyocr(image_path)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        print("✅ OCR works on valid image")

    def test_missing_image(self):
        """Test OCR with a missing image file."""
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../images/nonexisting_image.png')
        with self.assertRaises(FileNotFoundError):
            extract_text_easyocr(image_path)
        print("✅ OCR raises error for missing image")

    if __name__ =='__main__':
        unittest.main()
