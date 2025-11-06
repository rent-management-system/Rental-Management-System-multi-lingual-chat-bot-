from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user's query in any supported language.")
    language: Optional[Literal["english", "amharic", "afaan_oromo"]] = Field(
        None, description="Optional: Forces the response language. If not provided, language is auto-detected."
    )

    @field_validator('language', mode='before')
    @classmethod
    def language_to_lower(cls, v: str) -> str:
        if v:
            return v.lower()
        return v
