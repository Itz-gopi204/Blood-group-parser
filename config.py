import os

class Config:
    # Secret key used for token-based authentication
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
    # Tesseract OCR command path (set this if Tesseract is not in your PATH)
    TESSERACT_CMD = os.environ.get("TESSERACT_CMD", "tesseract")
    # Languages for OCR; for multi-language support you could use something like "eng+hin"
    OCR_LANGUAGES = os.environ.get("OCR_LANGUAGES", "eng")
    # Directory to temporarily store uploaded files
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    # Allowed file extensions for upload
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.pdf'}
