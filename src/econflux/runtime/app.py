from typing import Any, Dict

from bedrock_agentcore.runtime import BedrockAgentCoreApp

from econflux.agent import build_agent

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

    You can extend this later to include user_id, language, or options.
    """
    user_prompt = payload.get("prompt")
    if not user_prompt:
        return {"error": "Missing 'prompt' in payload."}

    response = _agent(user_prompt)

    return {
        "result": str(response),
    }


if __name__ == "__main__":
    # Local development server
    app.run()
