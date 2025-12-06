import boto3
import json
import os


def lambda_handler(event, context):
    try:
        # Get prompt from Lambda event
        if "prompt" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required parameter: prompt"}),
            }

        prompt = event["prompt"]

        # Get ARN and session ID from environment or use defaults
        agent_runtime_arn = os.environ.get(
            "AGENT_RUNTIME_ARN",
            "arn:aws:bedrock-agentcore:us-east-1:128959305403:runtime/econflux-dy8zRo8vNZ",
        )
        runtime_session_id = os.environ.get(
            "RUNTIME_SESSION_ID", "dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt"
        )
        qualifier = os.environ.get("QUALIFIER", "ECONFLUX")

        # Initialize Bedrock AgentCore client
        client = boto3.client("bedrock-agentcore", region_name="us-east-1")

        # Prepare payload
        payload = json.dumps({"prompt": prompt})

        # Invoke agent runtime
        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            runtimeSessionId=runtime_session_id,
            payload=payload,
            qualifier=qualifier,
        )

        # Process response
        response_body = response["response"].read()
        response_data = json.loads(response_body)

        # Return successful response
        return {"statusCode": 200, "body": json.dumps(response_data)}

    except Exception as e:
        # Handle exceptions
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
