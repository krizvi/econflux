from typing import List

from strands import Agent
from strands.models import BedrockModel

from econflux.config import load_model_config
from econflux.tools import (
    get_stock_price,
    get_price_history,
    get_earnings,
    generate_stock_report,
)


def build_agent() -> Agent:
    """
    Construct the EconFlux Strands agent with Bedrock model and yfinance tools.
    """
    cfg = load_model_config()

    # if not cfg.model_id:
    #     raise RuntimeError("BEDROCK_MODEL_ID must be set in environment or .env file.")

    model = BedrockModel(
        model_id=cfg.model_id,
        guardrail_id=cfg.guardrail_id,
        guardrail_version=cfg.guardrail_version,
    )

    # system_prompt = (
    #     "You are EconFlux, a financial intelligence assistant. "
    #     "You use tools to fetch real market data (prices, history, earnings) and generate "
    #     "clear, structured, and concise answers for economists and analysts. "
    #     "Always be explicit when you are using real data, and avoid guessing. "
    #     "When appropriate, summarize key numbers in bullet points."
    # )

    tools: List[object] = [
        get_stock_price,
        get_price_history,
        get_earnings,
        generate_stock_report,
    ]

    agent = Agent(
        model=model,
        # system_prompt=system_prompt,
        tools=tools,
    )

    return agent
