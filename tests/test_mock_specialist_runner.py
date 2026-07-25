from datetime import date

from agents.specialists.mock_specialist_runner import (
    MockSpecialistRunner,
)

from models.patient import (
    Diagnosis,
    LabResult,
    Medication,
    Patient,
    Sex,
)

from models.patient_context import (
    PatientContext,
    SpecialistType,
)

from models.specialist_output import (
    GuidelineStrength,
    Recommendation,
    SpecialistOutput,
)


def nephrology_rule(
    output,
    patient_context,
):

    egfr = patient_context.patient.labs.get(
        "eGFR"
    )

    if egfr is None:
        return

    for recommendation in output.recommendations:

        if recommendation.drug_name.lower() == "metformin":

            recommendation.contraindicated = (
                egfr.value < 30
            )


base_output = SpecialistOutput(

    specialist=SpecialistType.NEPHROLOGY,

    confidence=0.95,

    recommendations=[

        Recommendation(

            drug_name="Metformin",

            contraindicated=False,

            clinical_reason="Temporary",

            guideline_source="KDIGO",

            guideline_strength=GuidelineStrength.STRONG,

        )

    ],

)

runner = MockSpecialistRunner(

    cached_outputs={

        SpecialistType.NEPHROLOGY: base_output,

    },

    rules={

        SpecialistType.NEPHROLOGY: nephrology_rule,

    },

)

# ------------------------
# Case 1
# eGFR = 28
# ------------------------

patient1 = Patient(

    patient_id="P1",

    age=68,

    sex=Sex.MALE,

    diagnoses=[

        Diagnosis(name="CKD")

    ],

    medications=[

        Medication(

            name="Metformin",

            dose="500mg",

            frequency="BD",

        )

    ],

    labs={

        "eGFR": LabResult(

            value=28,

            unit="mL/min/1.73m²",

            recorded_at=date.today(),

        )

    },

)

context1 = PatientContext(

    patient=patient1,

    clinical_summary="",

    active_specialists=[

        SpecialistType.NEPHROLOGY

    ],

    primary_conditions=[],

    key_risks=[],

    missing_information=[],

)

result = runner.run(

    SpecialistType.NEPHROLOGY,

    context1,

    "",

)

print("=" * 70)

print("Case 1")

print("=" * 70)

print(

    result.recommendations[0].contraindicated

)

assert (

    result.recommendations[0].contraindicated

    is True

)

# ------------------------
# Case 2
# eGFR = 45
# ------------------------

patient2 = patient1.model_copy(
    deep=True
)

patient2.labs["eGFR"].value = 45

context2 = context1.model_copy(
    deep=True
)

context2.patient = patient2

result = runner.run(

    SpecialistType.NEPHROLOGY,

    context2,

    "",

)

print()

print("=" * 70)

print("Case 2")

print("=" * 70)

print(

    result.recommendations[0].contraindicated

)

assert (

    result.recommendations[0].contraindicated

    is False

)

print()

print("SUCCESS")