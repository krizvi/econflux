from typing import List

from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, retrieve, use_llm


from config import load_model_config
from market_tools import (
    get_stock_price,
    get_price_history,
    get_earnings,
    generate_stock_report,
)

from health_check_tools import ping
from rag_tools import (
    query_monetary_policy_kb,
    query_regulatory_changes_kb,
    query_policy_decisions_kb,
    query_economic_indicators_kb,
)


def build_agent() -> Agent:
    """
    Construct the EconFlux Strands agent with Bedrock model and yfinance tools.
    """
    cfg = load_model_config()
    print(f"modelID:{cfg.model_id}")

    # if not cfg.model_id:
    #     raise RuntimeError("BEDROCK_MODEL_ID must be set in environment or .env file.")

    model = BedrockModel(
        model_id=cfg.model_id,
        guardrail_id=cfg.guardrail_id,
        guardrail_version=cfg.guardrail_version,
    )

    system_prompt = """
    You are EconFlux, a financial intelligence assistant with expertise in economics and market analysis.

    Primary purpose: Provide accurate, concise, and data-driven financial insights using real-time market data and authoritative knowledge sources.

    When responding:
    - Always use available tools to fetch real-time data instead of making assumptions
    - Present numerical information in structured formats (bullet points, tables) for clarity
    - Cite your sources when drawing from knowledge bases with [Source: X]
    - Format any citations you receive in responses as proper footnotes or inline citations
    - Generate visualizations when they add value to numerical analysis
    - Balance technical precision with accessible explanations

    Available tools:
    1. Market data retrieval (real-time prices, historical data, earnings reports)
    2. Analytical functions (calculations, trend analysis, report generation)
    3. Knowledge bases (economic indicators, monetary policy, policy decisions, regulatory changes)
    4. Supplemental capabilities (calculator, LLM for edge cases)

    Your responses should demonstrate both financial expertise and practical utility for economists, analysts, and financial decision-makers.
    """

    tools: List[object] = [
        get_stock_price,
        get_price_history,
        get_earnings,
        generate_stock_report,
        ping,
        calculator,
        retrieve,
        query_economic_indicators_kb,
        query_monetary_policy_kb,
        query_policy_decisions_kb,
        query_regulatory_changes_kb,
        use_llm,
    ]

    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=tools,
    )

    return agent
