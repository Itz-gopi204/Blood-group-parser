from utils.unit_conversion import convert_unit
from utils.validation import validate_parameter

def normalize_parameters(extracted_params):
    """
    Normalize and validate extracted parameters.
    - Converts values to standard units.
    - Checks numerical ranges against clinical reference ranges.
    
    Returns a tuple: (normalized_parameters, errors)
    """
    normalized = {}
    errors = {}
    for param, data in extracted_params.items():
        if data is None:
            errors[param] = "Parameter not found."
            continue
        
        value = data.get("value")
        unit = data.get("unit")
        try:
            value_float = float(value)
        except ValueError:
            errors[param] = f"Invalid numeric value: {value}"
            continue
        
        # Convert to standard units (if needed)
        standard_value, standard_unit = convert_unit(param, value_float, unit)
        
        # Validate parameter against dummy clinical ranges
        valid, message = validate_parameter(param, standard_value)
        if not valid:
            errors[param] = message
        
        normalized[param] = {"value": standard_value, "unit": standard_unit}
    
    return normalized, errors
