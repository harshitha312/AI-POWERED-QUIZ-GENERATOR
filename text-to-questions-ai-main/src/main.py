from preprocessing import load_image, resize_image, apply_gaussian_blur, enhance_contrast, apply_threshold
from src.ocr_easyocr import extract_text_easyocr


def main():
    image_path = 'C:/Users/Gunnam Harshitha/Desktop/Screenshots/Screenshot 2025-05-31 080233.png'


    try:
        # Step 1: Load and preprocess the image
        img = load_image(image_path)
        img = resize_image(img, scale_factor=2)          # Resize to improve OCR accuracy
        img = apply_gaussian_blur(img, kernel_size=7)    # Reduce noise
        img = enhance_contrast(img, factor=2.0)          # Increase contrast
        img = apply_threshold(img)                       # Convert to black and white

        # Step 2: Extract text using EasyOCR
        text = extract_text_easyocr(image_path)
        print("Extracted Text:\n", text)

    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()