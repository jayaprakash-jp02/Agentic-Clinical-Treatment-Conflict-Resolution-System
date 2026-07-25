from copy import deepcopy
from typing import Callable

from agents.specialists.specialist_runner import (
    SpecialistRunner,
)

from models.patient_context import (
    PatientContext,
    SpecialistType,
)

from models.specialist_output import (
    SpecialistOutput,
)


class MockSpecialistRunner(
    SpecialistRunner,
):
    """
    Development-only implementation.

    Uses simple rule functions instead of an LLM.

    Each specialist may optionally have a rule
    that updates its output based on the latest
    patient information.
    """

    def __init__(
        self,
        cached_outputs: dict[
            SpecialistType,
            SpecialistOutput,
        ],
        rules: dict[
            SpecialistType,
            Callable[
                [
                    SpecialistOutput,
                    PatientContext,
                ],
                None,
            ],
        ] | None = None,
    ):

        self.cached_outputs = cached_outputs

        self.rules = rules or {}

    def run(
    self,
    specialist,
    patient_context,
) -> SpecialistOutput:

        output = deepcopy(

            self.cached_outputs[
                specialist
            ]

        )

        rule = self.rules.get(
            specialist
        )

        if rule is not None:

            rule(
                output,
                patient_context,
            )

        return output