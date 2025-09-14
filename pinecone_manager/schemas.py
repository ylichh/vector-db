from pydantic import BaseModel
from typing import List, Optional


class VectorMetadata(BaseModel):
    command: str
    data: str


class VectorMatch(BaseModel):
    id: str
    score: float
    metadata: Optional[VectorMetadata] = None
    values: Optional[List[float]] = None


class VectorMatches(BaseModel):
    matches: List[VectorMatch]
