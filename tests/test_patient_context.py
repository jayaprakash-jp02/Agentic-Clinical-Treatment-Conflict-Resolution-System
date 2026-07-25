from models.patient import Patient
from models.patient_context import PatientContext, SpecialistType

patient = Patient(
    patient_id="P001",
    age=68,
    sex="Male",
    diagnoses=[
        {
            "name": "Type 2 Diabetes",
            "stage": "Type 2"
        },
        {
            "name": "Chronic Kidney Disease",
            "stage": "Stage 3b"
        }
    ],
    medications=[
        {
            "name": "Metformin",
            "dose": "500 mg",
            "frequency": "Twice Daily"
        }
    ],
    labs={
        "eGFR": {
            "value": 28,
            "unit": "mL/min/1.73m²",
            "recorded_at": "2026-04-01"
        }
    },
    vitals={
        "weight_kg": 78,
        "blood_pressure": {
            "systolic": 150,
            "diastolic": 92
        }
    },
    symptoms=["fatigue"],
    history=["Hypertension"]
)

context = PatientContext(
    patient=patient,
    clinical_summary=(
        "68-year-old male with Type 2 Diabetes, "
        "CKD Stage 3b and hypertension."
    ),
    active_specialists=[
        SpecialistType.ENDOCRINOLOGY,
        SpecialistType.NEPHROLOGY
    ],
    primary_conditions=[
        "Type 2 Diabetes",
        "CKD Stage 3b"
    ],
    key_risks=[
        "Reduced kidney function",
        "Poor glycemic control"
    ],
    missing_information=[
        "Urine Albumin"
    ]
)

print(context.model_dump())