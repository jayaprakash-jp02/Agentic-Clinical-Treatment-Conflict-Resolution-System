from models.patient import Patient

SPECIALIST_OPTIONS = [
    "Cardiology",
    "Nephrology",
    "Endocrinology",
]


def build_prompt(patient: Patient) -> str:
    diagnoses = "\n".join(
        f"- {d.name}" + (f" ({d.stage})" if d.stage else "")
        for d in patient.diagnoses
    )

    medications = "\n".join(
        f"- {m.name} | Dose: {m.dose} | Frequency: {m.frequency}"
        for m in patient.medications
    )

    labs = "\n".join(
      (
        f"- {name}:\n"
        f"    Value: {lab.value}\n"
        f"    Unit: {lab.unit}\n"
        f"    Recorded: {lab.recorded_at}"
      )
       for name, lab in patient.labs.items()
    )

    history = (
        "\n".join(f"- {item}" for item in patient.history)
        if patient.history
        else "None"
    )

    allergies = (
        "\n".join(f"- {item}" for item in patient.allergies)
        if patient.allergies
        else "None"
    )

    symptoms = (
        "\n".join(f"- {item}" for item in patient.symptoms)
        if patient.symptoms
        else "None"
    )

    if patient.vitals:
        vitals = (
            f"Weight: {patient.vitals.weight_kg} kg\n"
            f"Blood Pressure: "
            f"{patient.vitals.blood_pressure.systolic}/"
            f"{patient.vitals.blood_pressure.diastolic} mmHg"
        )
    else:
        vitals = "Not Available"

    return f"""
You are a clinical patient understanding agent.

Your responsibility is ONLY to understand the patient's clinical profile.

DO NOT recommend treatments.

DO NOT recommend medications.

DO NOT retrieve guidelines.

DO NOT explain reasoning.

Your only task is to summarize the patient and determine which specialist agents should participate.

Supported specialist agents:

{", ".join(SPECIALIST_OPTIONS)}

Patient Information

Age: {patient.age}

Sex: {patient.sex.value}

Diagnoses

{diagnoses}

Current Medications

{medications}

Laboratory Results

{labs}

Symptoms

{symptoms}

Past Medical History

{history}

Allergies

{allergies}

Vital Signs

{vitals}

Rules

1. Return ONLY valid JSON.

2. Do NOT return Markdown.

3. Do NOT return explanations.

4. Choose specialists ONLY from the supported specialist list.

5. Select at least ONE specialist.

6. Keep summaries concise.

Return exactly this JSON format:

{{
    "clinical_summary": "...",

    "active_specialists": [
        "Cardiology"
    ],

    "primary_conditions": [
        "..."
    ],

    "key_risks": [
        "..."
    ],

    "missing_information": [
        "..."
    ]
}}
""".strip()