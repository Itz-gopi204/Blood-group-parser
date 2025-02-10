import cv2
import pytesseract
from config import Config

# Set tesseract command path if needed
pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD

def preprocess_image(image_path):
    """
    Preprocess the image for OCR by:
    - Converting to grayscale.
    - Reducing noise using bilateral filtering and median blur.
    - Applying adaptive thresholding.
    
    Returns the path to a temporary preprocessed image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unreadable.")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Noise reduction using bilateral filter
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Apply median blur
    blurred = cv2.medianBlur(denoised, 3)
    
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Save the preprocessed image to a temporary file
    temp_filename = "temp_processed.png"
    cv2.imwrite(temp_filename, thresh)
    
    return temp_filename

def perform_ocr(image_path, language="eng"):
    """
    Perform OCR on the preprocessed image with support for multiple languages.
    """
    text = pytesseract.image_to_string(image_path, lang=language)
    return text
