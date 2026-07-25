from models.patient import Patient
from agents.patient_understanding.agent import (
    run_patient_understanding,
)

patient = Patient(
    patient_id="P001",
    age=68,
    sex="Male",
    diagnoses=[
        {
            "name": "Type 2 Diabetes",
            "stage": "Type 2",
        },
        {
            "name": "Chronic Kidney Disease",
            "stage": "Stage 3b",
        },
    ],
    medications=[
        {
            "name": "Metformin",
            "dose": "500 mg",
            "frequency": "Twice Daily",
        }
    ],
    labs={
        "eGFR": {
            "value": 28,
            "unit": "mL/min/1.73m²",
            "recorded_at": "2026-04-01",
        }
    },
    history=[
        "Hypertension"
    ],
    symptoms=[
        "Fatigue"
    ],
    vitals={
        "weight_kg": 78,
        "blood_pressure": {
            "systolic": 150,
            "diastolic": 92,
        },
    },
)

context = run_patient_understanding(patient)

print(context.model_dump())