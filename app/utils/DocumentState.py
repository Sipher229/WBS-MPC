from enum import StrEnum


class DocumentState(StrEnum):
    PENDING = "pending"
    PROCESSED = "processed"
    NORMALIZED = "normalized"
