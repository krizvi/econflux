import logging
import argparse
import os
from typing import Any, Dict

from bedrock_agentcore.runtime import BedrockAgentCoreApp

from core_agent import build_agent

# Custom TRACE level
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")


def _trace(self, msg, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, msg, args, **kwargs)


logging.Logger.trace = _trace


def parse_level(value: str) -> int:
    value = value.upper()
    if value == "TRACE":
        return TRACE_LEVEL
    return getattr(logging, value, logging.INFO)


def configure_logging(log_level: str = None) -> None:
    """Configure logging with specified level or default to INFO."""
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")

    logging.basicConfig(
        level=parse_level(log_level),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,  # Reconfigure if already set
    )


logger = logging.getLogger(__name__)

# Build the agent once at startup
_agent = build_agent()

# Create the AgentCore wrapper
app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entrypoint for EconFlux.

    Expected payload shape:
      {"prompt": "<user question>"}
    """
    user_prompt = payload.get("prompt")
    if not user_prompt:
        logger.error("Missing 'prompt' in payload")
        return {"error": "Missing 'prompt' in payload."}

    logger.info(f"Processing prompt: {user_prompt[:50]}...")
    response = _agent(user_prompt)
    logger.debug(f"Agent response: {response}")

    return {"result": str(response)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EconFlux Agent Server")
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Logging level (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    args = parser.parse_args()

    configure_logging(args.log_level)

    # Enable BedrockAgentCoreApp's internal logger
    app_logger = logging.getLogger("bedrock_agentcore.app")
    app_logger.setLevel(args.log_level)

    # Enable uvicorn's logger to see startup messages
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(args.log_level)

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.setLevel(args.log_level)

    logger.info(f"Starting EconFlux with log level: {args.log_level}")

    # Map custom TRACE to DEBUG for uvicorn (it only accepts standard levels)
    uvicorn_log_level = (
        "debug" if args.log_level.upper() == "TRACE" else args.log_level.lower()
    )

    # Run with access_log enabled to see requests
    app.run()
