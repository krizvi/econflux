"""
RAG tools for querying Bedrock Knowledge Bases used by EconFlux.

Each tool targets a specific finance/economics corpus produced by the synthetic
data generator (monetary policy, economic indicators, regulatory changes,
policy decisions).

Tools follow the Strands @tool pattern and return structured
results ready for grounding answers.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import boto3
from botocore.config import Config
from strands import tool

_bedrock_runtime_client = None


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


def _retrieve_from_bedrock_kb(
    kb_id_env: str,
    kb_label: str,
    query: str,
    max_results: int,
) -> Dict[str, Any]:
    
    """Shared retrieval helper for all KB tools."""
    kb_id = os.getenv(kb_id_env)
    # print(f"Knowledge Base Id Env:{kb_id_env}--Knowledge Base Id:{kb_id}-- Knowledge Base Name:{kb_label}")
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


@tool
def query_monetary_policy_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about monetary policy summaries (rate decisions, stance, rationale).

    Use when answering central bank policy questions that need citations from the monetary
    policy corpus.

    Args:
        query: User question that should be answered with monetary policy context.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_bedrock_kb(
        kb_id_env="KB_MONETARY_POLICY_ID",
        kb_label="kb_monetary_policy_summaries",
        query=query,
        max_results=max_results,
    )


@tool
def query_economic_indicators_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about economic indicators (GDP, CPI, unemployment, PMIs).

    Use when summarizing macro releases or explaining indicator movements.

    Args:
        query: User question requiring indicator context.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_bedrock_kb(
        kb_id_env="KB_ECONOMIC_INDICATORS_ID",
        kb_label="kb_economic_indicators",
        query=query,
        max_results=max_results,
    )


@tool
def query_regulatory_changes_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about regulatory changes and compliance timelines.

    Use for sector rules, supervisory focus areas, and implementation guidance.

    Args:
        query: User question about regulations or compliance changes.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_bedrock_kb(
        kb_id_env="KB_REGULATORY_CHANGES_ID",
        kb_label="kb-regulatory-changes",
        query=query,
        max_results=max_results,
    )


@tool
def query_policy_decisions_kb(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Retrieve grounded passages about policy decisions (vote splits, guidance, inflation context).

    Use for central banking decision rationale, forward guidance, and committee votes.

    Args:
        query: User question needing policy decision context.
        max_results: Maximum passages to return (1-10, default 5).

    Returns:
        Dict with:
        - knowledge_base: Friendly KB label
        - results: List of passages with score and source metadata, or empty list
        - error: Present if the KB ID is missing or Bedrock retrieval fails
    """
    return _retrieve_from_bedrock_kb(
        kb_id_env="KB_POLICY_DECISIONS_ID",
        kb_label="kb_policy_decisions",
        query=query,
        max_results=max_results,
    )
