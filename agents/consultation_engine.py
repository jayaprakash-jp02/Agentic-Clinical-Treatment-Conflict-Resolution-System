from agents.specialists.specialist_runner import SpecialistRunner

from models.patient_context import (
    PatientContext,
    SpecialistType,
)

from models.specialist_output import (
    SpecialistOutput,
)


class ConsultationEngine:
    """
    Runs every active specialist for the patient
    and collects their outputs.

    This class does NOT:
    - perform conflict resolution
    - negotiate
    - build consensus

    It only coordinates specialist execution.
    """

    def __init__(
        self,
        runner: SpecialistRunner,
    ):
        self.runner = runner

    def run_all(
        self,
        patient_context: PatientContext,
    ) -> dict[
        SpecialistType,
        SpecialistOutput,
    ]:

        outputs: dict[
            SpecialistType,
            SpecialistOutput,
        ] = {}

        for specialist in patient_context.active_specialists:

            outputs[specialist] = self.runner.run(
                specialist=specialist,
                patient_context=patient_context,
            )

        return outputs