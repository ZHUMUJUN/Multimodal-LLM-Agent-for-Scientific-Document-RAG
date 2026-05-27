from typing import List
from pydantic import BaseModel, Field

class QueryAnalysis(BaseModel):
    is_clear: bool = Field(
        description="Indicates if the user's question is clear and answerable."
    )
    questions: List[str] = Field(
        description="List of rewritten, self-contained questions."
    )
    clarification_needed: str = Field(
        description="Explanation if the question is unclear."
    )


class WorkerTask(BaseModel):
    role: str = Field(description="Worker role name, such as method_worker or data_eval_worker.")
    task: str = Field(description="Specific worker task to complete.")
    search_query: str = Field(description="Retrieval query the worker should use first.")
    expected_output: str = Field(description="What the worker should return to the synthesizer.")


class ReflectionDecision(BaseModel):
    is_answer_complete: bool = Field(description="Whether the draft answer fully addresses the worker task.")
    evidence_score: float = Field(description="Evidence sufficiency score from 0.0 to 1.0.")
    missing_aspects: List[str] = Field(default_factory=list, description="Important user-requested aspects missing from the draft answer.")
    unsupported_claims: List[str] = Field(default_factory=list, description="Claims in the draft answer that are not supported by retrieved evidence.")
    follow_up_queries: List[str] = Field(default_factory=list, description="Focused follow-up retrieval queries for missing or weakly supported aspects.")
    should_search_again: bool = Field(description="Whether the agent should perform another retrieval round before finalizing.")
