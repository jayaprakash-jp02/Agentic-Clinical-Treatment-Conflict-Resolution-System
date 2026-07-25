from models.criterion import Criterion
from models.patient_context import SpecialistType

criterion = Criterion(
    drug_name="Metformin",
    conflicting_specialists=[
        SpecialistType.ENDOCRINOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    depends_on_evidence=[
        "eGFR"
    ]
)

print(criterion.model_dump())