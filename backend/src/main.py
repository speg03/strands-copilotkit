import os
from datetime import datetime
from zoneinfo import ZoneInfo

from ag_ui_strands import StrandsAgent, StrandsAgentConfig, create_strands_app
from fastapi.middleware.cors import CORSMiddleware
from strands import Agent, tool
from strands.models import BedrockModel


@tool
def get_local_time(timezone: str = "UTC") -> str:
    """Return the current time for an IANA timezone such as Asia/Tokyo or UTC."""
    try:
        return datetime.now(ZoneInfo(timezone)).isoformat()
    except Exception:
        return f"Unknown timezone: {timezone}. Use an IANA timezone such as Asia/Tokyo."


model = BedrockModel(
    model_id=os.environ["BEDROCK_MODEL_ID"],
    region_name=os.environ["AWS_REGION"],
)

agent = Agent(
    model=model,
    tools=[get_local_time],
    system_prompt=(
        "You are a concise, helpful assistant. Use the get_local_time tool when "
        "the user asks for a current time or date in a timezone."
    ),
)

app = create_strands_app(
    StrandsAgent(
        agent=agent,
        name="bedrock_assistant",
        description="A Strands assistant powered by Amazon Bedrock.",
        config=StrandsAgentConfig(),
    ),
    "/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
