from utils.json_validator import JSONValidator

from knowledge.retriever import GuidelineRetriever
from llm.ollama_client import OllamaClient
from models.patient_context import (
    PatientContext,
    SpecialistType,
)
from models.specialist_output import SpecialistOutput
from prompts.specialist_prompt_builder import SpecialistPromptBuilder


class RealSpecialistRunner:
    """
    Runs a real specialist consultation using:

    PatientContext
            ↓
    Guideline Retrieval
            ↓
    Prompt Builder
            ↓
    Ollama
            ↓
    JSON Validation
            ↓
    SpecialistOutput
    """
    GUIDELINE_DIRECTORIES = {
    SpecialistType.CARDIOLOGY:
        "processed/AHA_ACC_HFSA_2022_Heart_Failure",

    SpecialistType.NEPHROLOGY:
        "processed/KDIGO_2024",

    SpecialistType.ENDOCRINOLOGY:
        "processed/ADA_2025",
}

    def __init__(
        self,
        retriever: GuidelineRetriever,
        prompt_builder: SpecialistPromptBuilder,
        llm: OllamaClient,
    ):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm

    def run(
    self,
    specialist: SpecialistType,
    patient_context: PatientContext,
) -> SpecialistOutput:

        # ----------------------------
        # Build retrieval query
        # ----------------------------

        query = (
            patient_context.clinical_summary
            + "\n"
            + " ".join(patient_context.primary_conditions)
            + "\n"
            + " ".join(patient_context.key_risks)
        )

        # ----------------------------
        # Retrieve guideline evidence
        # ----------------------------
        guideline_directory = self.GUIDELINE_DIRECTORIES.get(specialist)

        if guideline_directory is None:
            raise ValueError(
                f"No guideline directory configured for {specialist}"
            )
        retrieved_chunks = self.retriever.retrieve(
            query=query,
            guideline_directory=guideline_directory,
            top_k=5,
        )

        # ----------------------------
        # Build prompt
        # ----------------------------

        prompt = self.prompt_builder.build_prompt(
            specialist=specialist,
            patient_context=patient_context,
            retrieved_chunks=retrieved_chunks,
        )

        # ----------------------------
        # Call Ollama
        # ----------------------------

        raw_response = self.llm.generate(prompt)

        # ----------------------------
        # ----------------------------
        # Validate LLM response
        # ----------------------------

        return JSONValidator.validate(raw_response)