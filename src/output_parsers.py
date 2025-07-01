from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class ProfileSummary(BaseModel):
    summary: str = Field(description="summary of profile")
    facts: List[str] = Field(description="interesting facts about profile")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


profile_summary_parser = PydanticOutputParser(pydantic_object=ProfileSummary)
