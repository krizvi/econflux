"""RAG tools for querying Bedrock Knowledge Bases used by EconFlux.

Each tool targets a specific finance/economics corpus produced by the synthetic
data generator (monetary policy, economic indicators, regulatory changes,
policy decisions). Tools follow the Strands @tool pattern and return structured
results ready for grounding answers.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import boto3
from botocore.config import Config
from strands import tool

_bedrock_runtime_client = None
ANSWER_SYSTEM_PROMPT = """You are a finance and economics assistant. Use only the provided grounding passages to answer. If the passages do not contain the answer, say you cannot find it. Be concise."""


def _get_bedrock_runtime():
    """Lazily create and cache the Bedrock Agent Runtime client."""
    global _bedrock_runtime_client
    if _bedrock_runtime_client is not None:
        return _bedrock_runtime_client

    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    _bedrock_runtime_client = boto3.client(
        "bedrock-agent-runtime",
        region_name=region,
        config=Config(retries={"max_attempts": 3}),
    )
    return _bedrock_runtime_client


def _retrieve_from_kb(
    kb_id_env: str,
    kb_label: str,
    query: str,
    max_results: int,
) -> Dict[str, Any]:
    """Shared retrieval helper for all KB tools."""
    kb_id = os.getenv(kb_id_env)
    if not kb_id:
        return {
            "knowledge_base": kb_label,
            "error": f"Missing {kb_id_env} environment variable for {kb_label}.",
        }

    max_results = max(1, min(max_results, 10))
    client = _get_bedrock_runtime()

    try:
        response = client.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": max_results,
                }
            },
        )

        results: List[Dict[str, Any]] = []
        for item in response.get("retrievalResults", []):
            content = item.get("content", {}).get("text", "")
            score = item.get("score")
            location = item.get("location", {})

            results.append(
                {
                    "text": content,
                    "score": score,
                    "source": location.get("s3Location") or location or None,
                }
            )

        return {"knowledge_base": kb_label, "results": results}
    except Exception as exc:  # pragma: no cover - defensive error guard
        return {
            "knowledge_base": kb_label,
            "error": str(exc),
        }


def _format_passages(passages: List[Dict[str, Any]]) -> str:
    """Render retrieval passages into a newline-joined string for the LLM."""
    if not passages:
        return "No grounding passages found."

    formatted = []
    for idx, item in enumerate(passages, start=1):
        text = item.get("text") or ""
        score = item.get("score")
        source = item.get("source")
        meta_parts = []
        if score is not None:
            meta_parts.append(f"score={score}")
        if source:
            meta_parts.append(f"source={source}")
        meta = f" ({'; '.join(meta_parts)})" if meta_parts else ""
        formatted.append(f"{idx}. {text}{meta}")
    return "\n".join(formatted)


@tool
def query_monetary_policy_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about monetary policy summaries (rate decisions, stance, rationale).

    Use when answering central bank policy questions that need citations from the monetary
    policy corpus. Requires env var KB_MONETARY_POLICY_ID with the Bedrock KB ID.

    Args:
        query: User question that should be answered with monetary policy context.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_kb(
        kb_id_env="KB_MONETARY_POLICY_ID",
        kb_label="monetary_policy_summaries",
        query=query,
        max_results=max_results,
    )


@tool
def query_economic_indicators_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about economic indicators (GDP, CPI, unemployment, PMIs).

    Use when summarizing macro releases or explaining indicator movements. Requires
    env var KB_ECONOMIC_INDICATORS_ID with the Bedrock KB ID.

    Args:
        query: User question requiring indicator context.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_kb(
        kb_id_env="KB_ECONOMIC_INDICATORS_ID",
        kb_label="economic_indicators",
        query=query,
        max_results=max_results,
    )


@tool
def query_regulatory_changes_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about regulatory changes and compliance timelines.

    Use for sector rules, supervisory focus areas, and implementation guidance.
    Requires env var KB_REGULATORY_CHANGES_ID with the Bedrock KB ID.

    Args:
        query: User question about regulations or compliance changes.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_kb(
        kb_id_env="KB_REGULATORY_CHANGES_ID",
        kb_label="regulatory_changes",
        query=query,
        max_results=max_results,
    )


@tool
def query_policy_decisions_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about policy decisions (vote splits, guidance, inflation context).

    Use for central banking decision rationale, forward guidance, and committee votes.
    Requires env var KB_POLICY_DECISIONS_ID with the Bedrock KB ID.

    Args:
        query: User question needing policy decision context.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_kb(
        kb_id_env="KB_POLICY_DECISIONS_ID",
        kb_label="policy_decisions",
        query=query,
        max_results=max_results,
    )


def answer_with_kb(
    agent,
    query: str,
    kb: str = "monetary_policy",
    max_results: int = 5,
    system_prompt: str = ANSWER_SYSTEM_PROMPT,
) -> Dict[str, Any]:
    """
    Run a simple RAG loop: retrieve from a KB, then have the LLM answer using only that context.

    This helper expects `use_llm` to be registered on `agent.tool` (from strands-agents-tools).
    It does not register any tools; call it from your app code after constructing the Agent.

    Args:
        agent: Strands Agent with `use_llm` registered (e.g., tools=[use_llm, ...]).
        query: User question to ground.
        kb: Which KB to query: one of {"monetary_policy", "economic_indicators", "regulatory_changes", "policy_decisions"}.
        max_results: Max retrieval passages (1-10).
        system_prompt: System prompt for the LLM answer step.

    Returns:
        Dict with:
        - knowledge_base: KB label used
        - results: Passages from retrieval (may be empty)
        - answer: LLM answer text (string) when retrieval succeeded
        - error: Present if retrieval failed or use_llm raised
    """
    kb_map = {
        "monetary_policy": query_monetary_policy_kb,
        "economic_indicators": query_economic_indicators_kb,
        "regulatory_changes": query_regulatory_changes_kb,
        "policy_decisions": query_policy_decisions_kb,
    }

    if kb not in kb_map:
        return {"error": f"Unknown kb '{kb}'. Expected one of {list(kb_map)}"}

    retrieval = kb_map[kb](query=query, max_results=max_results)
    if retrieval.get("error"):
        return {
            "knowledge_base": retrieval.get("knowledge_base"),
            "error": retrieval["error"],
        }

    passages = retrieval.get("results", [])
    context_block = _format_passages(passages)

    prompt = (
        f'User question: "{query}"\n\n'
        f"Grounding passages:\n{context_block}\n\n"
        "Answer concisely using only the passages above."
    )

    try:
        llm_response = agent.tool.use_llm(
            prompt=prompt,
            system_prompt=system_prompt,
        )
        # normalize content to text
        text = llm_response
        if isinstance(llm_response, dict):
            content = llm_response.get("content")
            if content and isinstance(content, list) and content[0].get("text"):
                text = content[0]["text"]
        return {
            "knowledge_base": retrieval.get("knowledge_base"),
            "results": passages,
            "answer": text,
        }
    except Exception as exc:  # pragma: no cover - defensive guard
        return {
            "knowledge_base": retrieval.get("knowledge_base"),
            "results": passages,
            "error": str(exc),
        }
