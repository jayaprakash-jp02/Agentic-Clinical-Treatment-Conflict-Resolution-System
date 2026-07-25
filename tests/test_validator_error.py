from agents.patient_understanding.validator import validate_output

sample = {
    "clinical_summary": "Patient",
    "active_specialists": []
}

validate_output(sample)