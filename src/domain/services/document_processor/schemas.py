from pydantic import BaseModel
from typing import Any, Optional


class DocumentChunkData(BaseModel):
    text: str
    metadata: Optional[Any] = None


class CommandMetadata(BaseModel):
    command: str
    data: str


class CommandChunkData(DocumentChunkData):
    metadata: CommandMetadata
