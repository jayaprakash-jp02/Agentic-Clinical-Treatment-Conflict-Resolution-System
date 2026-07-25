import json

from models.patient_context import (
    PatientContext,
    SpecialistType,
)


class SpecialistPromptBuilder:
    """
    Builds prompts for specialist agents.
    """

    def build_prompt(
        self,
        specialist: SpecialistType,
        patient_context: PatientContext,
        retrieved_chunks: list[dict],
    ) -> str:

        guideline_context = "\n\n".join(
            [
                f"[{chunk['guideline']}]\n{chunk['text']}"
                for chunk in retrieved_chunks
            ]
        )

        patient_json = json.dumps(
            patient_context.patient.model_dump(mode="json"),
            indent=2,
        )

        json_schema = """
{
  "specialist": "Cardiology | Nephrology | Endocrinology",
  "recommendations": [
    {
      "drug_name": "...",
      "contraindicated": false,
      "clinical_reason": "...",
      "guideline_source": "...",
      "guideline_strength": "Strong",
      "depends_on_evidence": []
    }
  ],
  "confidence": 0.85,
  "missing_evidence": []
}
"""

        primary_conditions = "\n".join(
            f"- {condition}"
            for condition in patient_context.primary_conditions
        )

        key_risks = "\n".join(
            f"- {risk}"
            for risk in patient_context.key_risks
        )

        missing_information = "\n".join(
            f"- {info}"
            for info in patient_context.missing_information
        )

        if not primary_conditions:
            primary_conditions = "None"

        if not key_risks:
            key_risks = "None"

        if not missing_information:
            missing_information = "None"

        prompt = f"""
You are an expert {specialist.value} physician.

Your responsibility is ONLY to analyse the patient
from the perspective of your own specialty.

Never assume facts that are not provided.

==================================================
CLINICAL SUMMARY
==================================================

{patient_context.clinical_summary}

==================================================
PRIMARY CONDITIONS
==================================================

{primary_conditions}

==================================================
KEY RISKS
==================================================

{key_risks}

==================================================
MISSING INFORMATION
==================================================

{missing_information}

==================================================
PATIENT DATA
==================================================

{patient_json}

==================================================
RELEVANT GUIDELINES
==================================================

{guideline_context}

==================================================
TASK
==================================================

Using ONLY the supplied patient information and
guideline excerpts:

1. Evaluate the patient ONLY from the perspective
   of your specialty.

2. Review every current medication.

3. For each recommendation provide:
   - drug_name
   - contraindicated
   - clinical_reason
   - guideline_source
   - guideline_strength
   - depends_on_evidence

4. If important laboratory evidence is missing,
   include it in missing_evidence.

5. Assign an overall confidence score between
   0.0 and 1.0.

Return ONLY valid JSON using this schema:

{json_schema}

Rules:

- Use ONLY the supplied guideline evidence.
- Do NOT invent medications.
- Do NOT assume laboratory values that are not provided.
- Do NOT return markdown.
- Do NOT wrap JSON inside ``` blocks.
- Return valid JSON only.
"""

        return prompt.strip()