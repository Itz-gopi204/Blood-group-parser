def convert_unit(param, value, unit):
    """
    Convert the given value and unit to a standard unit for the parameter.
    For demonstration:
    - Hemoglobin: remains in g/dL.
    - WBC: remains in cells/µL.
    - Platelets: remains in cells/µL.
    - Cholesterol: remains in mg/dL.
    
    In production, add conversion logic if values are reported in different units.
    """
    # For demonstration purposes, we assume no conversion is required.
    standard_unit = unit  # Could be replaced with a mapping logic.
    return value, standard_unit
