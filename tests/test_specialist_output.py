from models.patient_context import SpecialistType
from models.specialist_output import (
    GuidelineStrength,
    Recommendation,
    SpecialistOutput,
)

output = SpecialistOutput(
    specialist=SpecialistType.NEPHROLOGY,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=True,
            clinical_reason=(
                "Risk of lactic acidosis in advanced CKD."
            ),
            guideline_source="KDIGO 2024",
            guideline_strength=GuidelineStrength.STRONG,
            depends_on_evidence=["eGFR"]
        ),
        Recommendation(
            drug_name="Empagliflozin",
            contraindicated=False,
            clinical_reason=(
                "Provides renal protection in eligible CKD patients."
            ),
            guideline_source="KDIGO 2024",
            guideline_strength=GuidelineStrength.STRONG,
            depends_on_evidence=["eGFR"]
        )
    ],
    confidence=0.94,
    missing_evidence=[
        "Recent Urine Albumin"
    ]
)

print(output.model_dump())