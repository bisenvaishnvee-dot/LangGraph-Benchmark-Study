import os
from typing import Any

from src.state import AgentState


def _get_llm() -> Any:
    """Return a chat model when a key is configured; otherwise use demo mode."""
    if not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "OPENAI_API_KEY is set but langchain-openai is unavailable. "
            "Install dependencies with: pip install -r requirements.txt"
        ) from exc
    return ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"), temperature=0)


def router_node(state: AgentState) -> AgentState:
    question = state.get("question", "")
    lower = question.lower()
    coding_terms = ("python", "code", "function", "program", "bug", "debug", "algorithm", "write a script")
    route = "coding" if any(term in lower for term in coding_terms) else "general"
    return {"route": route}


def answer_node(state: AgentState) -> AgentState:
    question = state.get("question", "")
    llm = _get_llm()

    if llm is None:
        # Clearly labeled, deterministic examples keep the repository runnable without a key.
        lower = question.lower()
        if "mmlu" in lower:
            answer = (
                "MMLU (Massive Multitask Language Understanding) evaluates broad knowledge "
                "across many academic subjects using multiple-choice questions. This is a "
                "demonstration response, not a benchmark result."
            )
        elif "photosynthesis" in lower:
            answer = (
                "Photosynthesis is the process by which plants use light energy to convert "
                "carbon dioxide and water into sugars, releasing oxygen as a by-product. "
                "This is a demonstration response."
            )
        else:
            answer = (
                "Demo mode is active, so no language model generated this answer. "
                "Set OPENAI_API_KEY to enable hosted-LLM responses. Your question was: "
                f"{question}"
            )
        return {"draft_answer": answer, "model_used": "demo"}

    prompt = (
        "You are one node in a LangGraph educational agent workflow. Answer clearly and "
        "state uncertainty when needed. Do not claim that a benchmark was run unless it was.\n\n"
        f"User question: {question}"
    )
    response = llm.invoke(prompt)
    usage = getattr(response, "usage_metadata", None) or {}
    answer = str(response.content)
    update: AgentState = {
        "draft_answer": answer,
        "model_used": os.getenv("LLM_MODEL", "gpt-4o-mini"),
    }
    if isinstance(usage, dict):
        if usage.get("input_tokens") is not None:
            update["input_tokens"] = int(usage["input_tokens"])
        if usage.get("output_tokens") is not None:
            update["output_tokens"] = int(usage["output_tokens"])
    return update


def coding_node(state: AgentState) -> AgentState:
    question = state.get("question", "")
    llm = _get_llm()

    if llm is None:
        answer = (
            "Demo coding path selected. No code-generating LLM is configured, so this is "
            "not a generated solution. Set OPENAI_API_KEY to enable code generation. "
            f"Task received: {question}"
        )
        return {"draft_answer": answer, "model_used": "demo"}

    prompt = (
        "You are the coding node in a LangGraph workflow. Provide a concise Python solution, "
        "explain key assumptions, and include a small example where useful. Do not claim "
        "the code was executed or tested unless a test tool actually ran.\n\n"
        f"User task: {question}"
    )
    response = llm.invoke(prompt)
    usage = getattr(response, "usage_metadata", None) or {}
    update: AgentState = {
        "draft_answer": str(response.content),
        "model_used": os.getenv("LLM_MODEL", "gpt-4o-mini"),
    }
    if isinstance(usage, dict):
        if usage.get("input_tokens") is not None:
            update["input_tokens"] = int(usage["input_tokens"])
        if usage.get("output_tokens") is not None:
            update["output_tokens"] = int(usage["output_tokens"])
    return update


def verification_node(state: AgentState) -> AgentState:
    draft = state.get("draft_answer", "")
    if not draft.strip():
        return {
            "verification_note": "No draft answer was produced; check the previous node.",
            "final_answer": "Sorry, the workflow did not produce an answer. Please try again.",
        }

    # This is a transparent heuristic, not factual verification.
    note = (
        "Draft is non-empty. This lightweight check does not verify factual correctness, "
        "run code, or replace a trusted evaluator."
    )
    return {"verification_note": note, "final_answer": draft}
