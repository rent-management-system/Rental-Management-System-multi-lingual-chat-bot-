from pydantic import BaseModel
from typing import List

class VectorItem(BaseModel):
    id: str
    embedding: List[float]
    document: str
