from flask import Flask, request, jsonify,render_template

import os

from config import Config
from modules.ocr_preprocesing import preprocess_image, perform_ocr
from modules.pdf_handler import convert_pdf_to_images
from modules.security import token_required, secure_store
from modules.audit import log_audit
from models.ner_model import extract_parameters_ner
from models.normalization import normalize_parameters

app = Flask(__name__)
app.config.from_object(Config)
# Frontend route to serve the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse-report', methods=['POST'])
@token_required
def parse_report():
    """
    Endpoint to parse a blood report.
    - Accepts a file upload (image or PDF).
    - Applies advanced preprocessing and OCR.
    - Extracts test parameters using a custom NER model.
    - Normalizes and validates the data.
    - Returns an EHR JSON response.
    """
    # Log audit details for security and compliance
    log_audit(request)

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in app.config['ALLOWED_EXTENSIONS']:
        return jsonify({"error": "Unsupported file format."}), 400
    
    # Securely store the file (includes encryption/decryption as demonstration)
    secure_file_path = secure_store(file, filename)

    # Process the file based on its extension (PDF or image)
    extracted_text = ""
    if ext == ".pdf":
        # Convert each PDF page to an image and process it
        image_paths = convert_pdf_to_images(secure_file_path)
        for img_path in image_paths:
            processed_img = preprocess_image(img_path)
            text = perform_ocr(processed_img, language=app.config['OCR_LANGUAGES'])
            extracted_text += text + "\n"
            # Clean up temporary image file
            os.remove(processed_img)
            os.remove(img_path)
    else:
        processed_img = preprocess_image(secure_file_path)
        extracted_text = perform_ocr(processed_img, language=app.config['OCR_LANGUAGES'])
        os.remove(processed_img)
    
    # Extract blood test parameters using a custom NER model
    extracted_params = extract_parameters_ner(extracted_text)
    
    # Normalize and validate the extracted parameters
    normalized_params, errors = normalize_parameters(extracted_params)
    
    # For demonstration, using static patient and lab info (in a real system these could be extracted)
    patient_info = {
        "name": "John Doe",
        "age": 35,
        "gender": "Male",
        "patient_id": "123456"
    }
    lab_info = {
        "lab_name": "ABC Diagnostic Labs",
        "report_date": "2025-02-10"
    }
    
    ehr = {
        "patient_info": patient_info,
        "lab_info": lab_info,
        "test_results": normalized_params,
        "validation_errors": errors
    }
    
    # Optionally, remove the secure file after processing
    os.remove(secure_file_path)
    
    return jsonify(ehr)

if __name__ == '__main__':
    app.run(debug=True)
