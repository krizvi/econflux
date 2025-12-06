import boto3
import json

PROMPT = "What ethical frameworks guide central bankers forward guidance during periods of high inflation versus high unemployment? Analyze the philosophical underpinnings of policy decisions and dissenting votes."


AGENT_RUNTIME_ARN = (
    "arn:aws:bedrock-agentcore:us-east-1:128959305403:runtime/econflux_app-ue5VAV2x2A"
)
RUNTIME_SESSION_ID = "dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt"
QUALIFIER = "EconfluxLambda"

client = boto3.client("bedrock-agentcore", region_name="us-east-1")
payload = json.dumps({"prompt": PROMPT})

response = client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_RUNTIME_ARN,
    runtimeSessionId=RUNTIME_SESSION_ID,
    payload=payload,
    qualifier=QUALIFIER,  # Optional
)
response_body = response["response"].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
