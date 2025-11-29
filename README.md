# EconFlux

EconFlux is an agentic financial intelligence service built with:

- [Strands-Agents](https://strandsagents.com/latest/documentation/docs/)
- [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/)
- [yfinance](https://pypi.org/project/yfinance/)

It exposes a single entrypoint that accepts a natural-language `prompt` and uses
yfinance-powered tools to fetch market data, then lets a Bedrock-backed model
reason about it.

## Features

- Live and recent price lookup
- Short-term price history
- Earnings snapshot and calendar
- Combined stock report tool
- Local development server and Bedrock AgentCore wrapper

## Quickstart

```bash
git clone <this-repo-url>
cd econflux
cp .env.example .env   # fill BEDROCK_MODEL_ID etc.
uv sync
uv pip install -e .
LOG_LEVEL=INFO uv run app.py
````

Then:

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Give me a 5-day summary of AAPL"}'
```

You will receive a JSON response with the model’s answer.

## Deploy the local code to Amamzon Bedrock AgentCore

```bash
agentcore configure --entrypoint ./econflux/runtime/app.py --name econflux
```

```bash
agentcore deploy --local
```

```bash
agentcore launch
```