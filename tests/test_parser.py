from agents.patient_understanding.parser import parse_response

raw = """
{
    "clinical_summary": "Patient has Type 2 Diabetes and CKD.",
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
"""

data = parse_response(raw)

print(type(data))

print(data)