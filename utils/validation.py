def validate_parameter(param, value):
    """
    Validate the parameter value against dummy clinical reference ranges.
    Returns (True, "") if valid, otherwise (False, error message).
    """
    # Dummy reference ranges for demonstration purposes.
    reference_ranges = {
        "Hemoglobin": (12.0, 18.0),    # in g/dL
        "WBC": (4000, 11000),          # in cells/µL
        "Platelets": (150000, 450000),  # in cells/µL
        "Cholesterol": (125, 200)       # in mg/dL
    }
    
    if param in reference_ranges:
        low, high = reference_ranges[param]
        if not (low <= value <= high):
            return False, f"{param} value {value} is out of normal range ({low}-{high})."
    
    return True, ""
