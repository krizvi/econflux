import boto3
import json

PROMPT="""
Conduct a peer analysis of Walmart, Target, and Costco as a table. 
Compare their price performance, earnings quality, and upcoming catalyst calendars. 
Which retailer presents the most compelling risk-reward profile right now?
"""

client = boto3.client("bedrock-agentcore", region_name="us-east-1")
payload = json.dumps({"prompt": PROMPT})

response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:128959305403:runtime/econflux-5nwkhPGvJS",
    runtimeSessionId="dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt",  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT",  # Optional
)
response_body = response["response"].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
