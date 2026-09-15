import os

from dotenv import load_dotenv
from agents import Agent
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from context import TWIN_SYSTEM_PROMPT
from tools import record_user_details

load_dotenv(override=True)

openrouter_client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

digital_twin = Agent(
    name="Digital Twin",
    instructions=TWIN_SYSTEM_PROMPT,
    tools=[record_user_details],
    model=OpenAIChatCompletionsModel(
        model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        openai_client=openrouter_client,
    ),
    
)