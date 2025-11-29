# EconFlux

EconFlux is an Agentic AI financial intelligence service built with [Strands-Agents](https://strandsagents.com/latest/documentation/docs/) and [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/). It is completely headless: there is no bundled UI client. You interact with it through HTTP (e.g., `curl`) when running locally, or via the `agentcore` CLI (e.g., `agentcore invoke`) when launched on Bedrock AgentCore.

At runtime the Bedrock model reasons over a Strands agent that is wired to a handful of tools for market lookups and health checks. The current tool implementations return mock market data to keep the project easy to run anywhere; you can swap in real data sources (such as `yfinance`) by updating `market_tools.py`.

## Capabilities

- Natural-language prompt entrypoint exposed as an AgentCore runtime.
- Mock stock price lookup, short-term price history, earnings snapshot, and combined stock report.
- Health check tool (`ping`) to verify the toolchain is reachable.
- Bedrock guardrail hooks and model selection configurable via environment variables.
- Roadmap: Streamlit UI client and additional tools for RAG-backed answers targeting central banking and economist workflows.

## Repository Layout

```
.
├── README.md                # You are here
├── LICENSE
└── src
    ├── app.py               # BedrockAgentCoreApp entrypoint (`invoke`) and logging setup
    ├── config.py            # Environment-driven configuration (model IDs, guardrail IDs, eval flag)
    ├── core_agent.py        # Strands agent construction with Bedrock model and tool registry
    ├── health_check_tools.py# Ping tool for liveness checks
    ├── market_tools.py      # Mock market data tools (price, history, earnings, combined report)
    ├── rag/                 # Synthetic data generator for finance/economics RAG corpora
    │   └── synthetic_data_gen.py  # Produces domain corpora (monetary policy, indicators, regulatory changes, policy decisions)
    ├── pyproject.toml       # Project metadata and dependencies (Python 3.12+)
    ├── requirements.txt     # Runtime dependencies mirror pyproject for non-uv workflows
    ├── requirements-dev.txt # Dev extras (AgentCore starter toolkit)
    └── uv.lock              # uv lockfile for reproducible installs
```

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) for dependency management (recommended).
- AWS credentials with Bedrock access when invoking a Bedrock model (standard `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optional `AWS_PROFILE`).
- Environment variables:
  - `BEDROCK_MODEL_ID` (default: `us.anthropic.claude-sonnet-4-20250514-v1:0`)
  - `GUARDRAIL_ID` (optional)
  - `GUARDRAIL_VERSION` (default: `DRAFT`)
  - `EVAL_MODE` (optional flag used by `config.py`)
  - `LOG_LEVEL` (optional; defaults to `INFO`)
- Dependency manifests: `pyproject.toml` (uv / PEP 621) and `requirements.txt` (kept in sync because `agentcore configure` currently reads from `requirements.txt`; this duplication should go away as AgentCore matures).

Create a `.env` file alongside the code in `src/` (or export environment variables before running). `config.py` loads it automatically.

## Setup After Cloning

```bash
git clone <repo-url>
cd econflux
# Populate src/.env with BEDROCK_MODEL_ID and AWS credentials/region if not already exported
cd src
cat <<'EOF' > .env
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
GUARDRAIL_ID=
GUARDRAIL_VERSION=DRAFT
LOG_LEVEL=INFO
AWS_REGION=us-east-1
EOF

uv sync            # installs dependencies into .venv
uv pip install -e .  # editable install so the CLI can import econflux
```

## Running Locally (Headless)

Run `uv` commands from within `src/` (where `pyproject.toml` lives). Run `agentcore` commands from the repository root using paths like `./src/app.py`.

### Option A: Direct dev server via `uv`

```bash
LOG_LEVEL=INFO uv run app.py
```

The Bedrock AgentCore runtime listens on `http://127.0.0.1:8080/invocations`. Call it with `curl`:

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Give me a 5-day summary of AAPL"}'
```

### Option B: Local AgentCore deployment

If you prefer to run through the AgentCore CLI locally:

```bash
agentcore configure --entrypoint ./src/app.py --name econflux
agentcore deploy --local
```

This also exposes `http://localhost:8080/invocations`, so use `curl` as above. Because EconFlux is headless, there is no local UI; HTTP is the way in.

## Launching to Amazon Bedrock AgentCore

When you are ready to host the agent on Bedrock AgentCore:

```bash
agentcore configure --entrypoint ./src/app.py --name econflux
agentcore launch      # Deploys to Bedrock AgentCore in your configured AWS account/region
```

Once launched, use the AgentCore CLI to invoke the hosted agent (no need for `curl`):

```bash
agentcore invoke --name econflux --text "Give me a 5-day summary of AAPL"
```

Optional helpful commands:

- `agentcore describe --name econflux` to inspect the deployed runtime.
- `agentcore logs --name econflux` to stream logs.

## How It Works

1. `app.py` creates a `BedrockAgentCoreApp` and exposes an `invoke(payload)` entrypoint. The payload must contain a `prompt`.
2. `core_agent.py` builds a Strands `Agent` backed by a `BedrockModel` (configured from environment variables) and registers available tools.
3. `market_tools.py` and `health_check_tools.py` provide the callable tools. They currently return mock data so the agent works offline; replace their internals with real data fetches to productionize.
4. The response is returned as JSON under `result` when called via HTTP or `agentcore invoke`.

## RAG Knowledge Bases (planned)

The `rag/synthetic_data_gen.py` script produces four finance/economics corpora that will be ingested into Amazon Bedrock Knowledge Bases to ground the agent’s answers:

- Monetary policy summaries: chronologies of central bank rate decisions, stances, and rationale to explain policy direction.
- Economic indicators: releases (GDP, CPI, unemployment, PMIs) with context to anchor macro commentary.
- Regulatory changes: sector-specific rules, compliance timelines, and supervisory focus areas to inform risk/reg policy answers.
- Policy decisions: vote splits, forward guidance, and inflation context to answer central banking queries.

Planned Bedrock KB names will mirror these domains (e.g., `kb_monetary_policy_summaries`, `kb_economic_indicators`, `kb_regulatory_changes`, `kb_policy_decisions`). These KBs will be mounted so the agent can cite grounded facts for central banking and economist users.

## Living Documentation and UI Plan

This README is a living document. Upcoming additions will cover:

- Streamlit UI details (for a lightweight client on top of the existing headless runtime).
- Four new tools to query the Bedrock knowledge bases above (monetary policy, indicators, regulatory, policy decisions) for RAG-grounded responses.
- Operational runbooks and deployment notes as AgentCore and the surrounding tooling evolve rapidly.

## Extending or Productionizing

- Swap mock implementations in `market_tools.py` with live data sources (e.g., `yfinance`, an internal market data API, or cached data stores).
- Add guardrails or moderation by setting `GUARDRAIL_ID`/`GUARDRAIL_VERSION`.
- Implement additional tools (news lookup, portfolio analytics) and register them in `core_agent.py`.
- Tighten logging verbosity with `LOG_LEVEL` or the `--log-level` flag when running `app.py`.

## Troubleshooting

- Missing `prompt` key results in `{"error": "Missing 'prompt' in payload."}`; ensure your JSON body includes `prompt`.
- Authentication errors from Bedrock mean your AWS credentials or region are not configured.
- If the runtime is up but you see no responses, confirm port `8080` is free and that you are POSTing to `/invocations`.
