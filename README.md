# Strands + CopilotKit + Amazon Bedrock

This sample runs a React/CopilotKit SPA and a Strands Agent in two local Docker containers. The browser communicates directly with the agent through AG-UI streaming. The agent invokes Amazon Bedrock and can call a local-time tool.

## Prerequisites

- Docker Desktop for macOS
- AWS CLI v2 configured with an IAM Identity Center profile
- Bedrock model access in the selected AWS Region

## Configure

Create `.env` from the example and set the profile, region, and an inference profile ID or ARN available to your account.

```sh
cp .env.example .env
```

Authenticate the profile on the host before starting containers:

```sh
aws sso login --profile "$AWS_PROFILE"
```

The backend receives only read-only mounts for `~/.aws/config` and `~/.aws/sso/cache`; no AWS access key is copied into the project or image.

### Bedrock inference profiles

Some current Bedrock models, including Claude Sonnet 4.6, cannot be invoked with on-demand throughput. Set `BEDROCK_INFERENCE_PROFILE_ID` to a cross-Region inference profile ID or an application inference profile ARN instead of the foundation model ID.

For Claude Sonnet 4.6 from `ap-northeast-1`, use:

```dotenv
BEDROCK_INFERENCE_PROFILE_ID=global.anthropic.claude-sonnet-4-6
```

After authenticating, list the profiles available to the configured profile and region with:

```sh
aws bedrock list-inference-profiles \
	--profile "$AWS_PROFILE" \
	--region "$AWS_REGION" \
	--type-equals SYSTEM_DEFINED \
	--query "inferenceProfileSummaries[?contains(inferenceProfileId, 'claude-sonnet-4-6')].[inferenceProfileId,inferenceProfileArn,status]" \
	--output table
```

## Run

```sh
docker compose up --build --wait
```

Open [http://localhost:5173](http://localhost:5173). Send a normal question, then ask for the current time in `Asia/Tokyo` to exercise the Strands tool.

The health endpoint is available at [http://localhost:8000/health](http://localhost:8000/health).

Stop the stack with:

```sh
docker compose down
```

## Troubleshooting

- If the backend cannot authenticate, run `aws sso login --profile <profile>` again on the host and restart the backend.
- If Bedrock reports that on-demand throughput is unsupported, replace the foundation model ID with its cross-Region inference profile ID or ARN in `BEDROCK_INFERENCE_PROFILE_ID`, then recreate the backend with `docker compose up --build --force-recreate backend`.
- If Bedrock rejects the request, confirm that the inference profile can be invoked from `AWS_REGION` and that the selected profile grants `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`.
- If the browser cannot connect, confirm that both services are healthy with `docker compose ps` and that port `5173` or `8000` is not occupied.