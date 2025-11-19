import cv2 as cv
import numpy as np
from PIL import Image, ImageEnhance

def load_image(image_path: str) ->np.ndarray:
    """Load an image from the given path and return as a NumPy array."""
    img = cv.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return img

def resize_image(img: np.ndarray, scale_factor: int) ->np.ndarray:
    return cv.resize(img, (img.shape[1] * scale_factor, img.shape[0] * scale_factor), interpolation=cv.INTER_LINEAR)
    
    
def apply_gaussian_blur(img: np.ndarray, kernel_size :int =7) ->np.ndarray:
    return cv.GaussianBlur(img, (kernel_size, kernel_size), 0)

def enhance_contrast(img: np.ndarray, factor: float)->np.ndarray:
    # Increase contrast using PIL
    pil_image = Image.fromarray(img)
    enhancer = ImageEnhance.Contrast(pil_image)
    return np.array(enhancer.enhance(factor))  # Enhance contrast

def apply_threshold(img: np.ndarray) ->np.ndarray:
    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale
    _,binary_img = cv.threshold(np.array(grayscale_img), 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return binary_img
    