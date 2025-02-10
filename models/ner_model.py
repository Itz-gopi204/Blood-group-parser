import spacy

# For demonstration, we use spaCy's pre-trained English model.
# In production, load a custom-trained NER model tuned for blood report entities.
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_parameters_ner(text):
    """
    Extract blood test parameters and their values using a custom NER approach.
    This demo uses a simple method by scanning for lines with ':'.
    In production, a custom-trained NER model would mark entities such as TEST_NAME, VALUE, and UNIT.
    """
    extracted = {}
    lines = text.splitlines()
    for line in lines:
        # A naive approach: look for patterns like "Hemoglobin: 13.5 g/dL"
        if ":" in line:
            parts = line.split(":", 1)
            param = parts[0].strip()
            value_unit = parts[1].strip()
            tokens = value_unit.split()
            if tokens:
                value = tokens[0]
                unit = " ".join(tokens[1:]) if len(tokens) > 1 else ""
                extracted[param] = {"value": value, "unit": unit}
    return extracted
