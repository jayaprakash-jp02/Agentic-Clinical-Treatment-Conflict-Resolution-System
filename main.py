from agents.consultation_engine import ConsultationEngine

from agents.conflict_resolution.engine import (
    ConflictResolutionEngine,
)

from agents.decision_support.decision_support_agent import (
    DecisionSupportAgent,
)

from agents.planner.consensus_builder import ConsensusBuilder
from agents.planner.evidence_replanner import EvidenceReplanner
from agents.planner.negotiation_loop import NegotiationLoop
from agents.planner.planner import Planner

from agents.specialists.real_specialist_runner import (
    RealSpecialistRunner,
)

from agents.patient_understanding.agent import (
    run_patient_understanding,
)

from knowledge.retriever import GuidelineRetriever
from llm.ollama_client import OllamaClient
from prompts.specialist_prompt_builder import (
    SpecialistPromptBuilder,
)

from models.consensus import ConsensusState
from models.patient import Patient
from state.negotiation_state import NegotiationState

import json


def load_patient(path: str) -> Patient:
    """
    Load and validate a patient JSON file.
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return Patient.model_validate(data)


def main():

    # -------------------------------------------------
    # Load Patient
    # -------------------------------------------------

    print("Step 1: Main started")

    patient = load_patient(
        "data/patients/patient1.json"
    )

    print("Step 2: Patient loaded")

    # -------------------------------------------------
    # Patient Understanding
    # -------------------------------------------------

    patient_context = run_patient_understanding(
        patient
    )

    print("Step 3: Patient context created")

    # -------------------------------------------------
    # Build Core Components
    # -------------------------------------------------

    retriever = GuidelineRetriever()

    prompt_builder = SpecialistPromptBuilder()

    llm = OllamaClient(
        model="qwen2.5:7b"
    )

    specialist_runner = RealSpecialistRunner(
        retriever=retriever,
        prompt_builder=prompt_builder,
        llm=llm,
    )

    consultation_engine = ConsultationEngine(
        specialist_runner
    )

    print("Step 4: Components created")

    # -------------------------------------------------
    # Run Specialists
    # -------------------------------------------------

    specialist_outputs = consultation_engine.run_all(
        patient_context
    )

    print("Step 5: Specialists completed")

    # -------------------------------------------------
    # Detect Conflicts
    # -------------------------------------------------

    conflict_engine = ConflictResolutionEngine()

    criteria = conflict_engine.build_criteria(
        specialist_outputs
    )

    print(f"Step 6: {len(criteria)} conflict(s) detected")

    # -------------------------------------------------
    # Negotiation State
    # -------------------------------------------------

    negotiation_state = NegotiationState(
        patient_context=patient_context,
        active_specialists=patient_context.active_specialists,
        specialist_outputs=specialist_outputs,
        unresolved_criteria=criteria,
        consensus_state=ConsensusState(),
    )

    print("Step 7: NegotiationState created")

    # -------------------------------------------------
    # Negotiation Components
    # -------------------------------------------------

    planner = Planner()

    replanner = EvidenceReplanner(
        specialist_runner
    )

    consensus_builder = ConsensusBuilder()

    negotiation_loop = NegotiationLoop(
        planner=planner,
        replanner=replanner,
        consensus_builder=consensus_builder,
    )

    print("Step 8: Negotiation Loop ready")

    # -------------------------------------------------
    # Run Negotiation
    # -------------------------------------------------

    final_state = negotiation_loop.run(
        negotiation_state
    )

    print("Step 9: Negotiation completed")

    # -------------------------------------------------
    # Generate Report
    # -------------------------------------------------

    decision_support = DecisionSupportAgent()

    report = decision_support.generate_report(
        final_state
    )

    print("\n================ FINAL REPORT ================\n")

    print(report)


if __name__ == "__main__":
    main()