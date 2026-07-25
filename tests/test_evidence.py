from models.evidence import (
    EvidenceRecord,
    EvidenceStatus,
)

record = EvidenceRecord(
    lab_name="eGFR",
    status=EvidenceStatus.REQUESTED,
    requested_reason=(
        "Updated eGFR could change Metformin eligibility."
    ),
    requested_at_iteration=1,
)

print(record.model_dump())