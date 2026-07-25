from enum import Enum
from typing import Optional

from pydantic import BaseModel

from models.patient import LabResult


class EvidenceStatus(str, Enum):
    REQUESTED = "Requested"
    RECEIVED = "Received"


class EvidenceRecord(BaseModel):
    lab_name: str

    status: EvidenceStatus

    requested_reason: str

    requested_at_iteration: int

    result: Optional[LabResult] = None