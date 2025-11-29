import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    model_id: str
    guardrail_id: str | None
    guardrail_version: str


@dataclass
class AppConfig:
    eval_mode: bool


def load_model_config() -> ModelConfig:
    return ModelConfig(
        model_id=os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-20250514-v1:0"),
        guardrail_id=os.getenv("GUARDRAIL_ID") or None,
        guardrail_version=os.getenv("GUARDRAIL_VERSION", "DRAFT"),
    )


def load_app_config() -> AppConfig:
    return AppConfig(
        eval_mode=os.getenv("EVAL_MODE", "false").lower() == "true",
    )
