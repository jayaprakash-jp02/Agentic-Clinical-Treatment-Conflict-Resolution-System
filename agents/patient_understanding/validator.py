from pydantic import BaseModel, Field


class PatientUnderstandingOutput(BaseModel):
    clinical_summary: str

    active_specialists: list[str] = Field(min_length=1)

    primary_conditions: list[str] = Field(default_factory=list)

    key_risks: list[str] = Field(default_factory=list)

    missing_information: list[str] = Field(default_factory=list)


def validate_output(data: dict) -> PatientUnderstandingOutput:
    return PatientUnderstandingOutput.model_validate(data)