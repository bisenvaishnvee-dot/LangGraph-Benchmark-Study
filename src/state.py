from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    route: str
    draft_answer: str
    verification_note: str
    final_answer: str
    model_used: str
    input_tokens: int
    output_tokens: int
