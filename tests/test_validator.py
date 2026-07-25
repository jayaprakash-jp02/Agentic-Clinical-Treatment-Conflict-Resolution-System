from agents.patient_understanding.validator import validate_output

sample = {
    "clinical_summary": "Patient has diabetes and CKD.",
    "active_specialists": [
        "Endocrinology",
        "Nephrology"
    ],
    "primary_conditions": [
        "Type 2 Diabetes",
        "CKD Stage 3b"
    ],
    "key_risks": [
        "Reduced kidney function"
    ],
    "missing_information": [
        "Recent HbA1c"
    ]
}

result = validate_output(sample)

print(result)

print(type(result))