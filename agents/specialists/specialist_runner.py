from abc import ABC, abstractmethod

from models.patient_context import (
    PatientContext,
    SpecialistType,
)

from models.specialist_output import (
    SpecialistOutput,
)


class SpecialistRunner(ABC):
    """
    Contract for executing a specialist.

    Implementations are responsible for:
    - retrieving relevant guideline evidence
    - performing specialist reasoning
    - returning a validated SpecialistOutput
    """

    @abstractmethod
    def run(
        self,
        specialist: SpecialistType,
        patient_context: PatientContext,
    ) -> SpecialistOutput:
        """
        Execute one specialist consultation.

        Parameters
        ----------
        specialist
            Specialist to execute.

        patient_context
            Current patient information.

        Returns
        -------
        SpecialistOutput
        """
        pass