import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.tools.recommend_tool import recommend_food
from app.tools.reserve_tool import reserve_food
from pydantic_ai.settings import ModelSettings

load_dotenv()

model = OpenAIChatModel(
    "gpt-4o-mini",
    provider=OpenAIProvider(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
)

agent = Agent(
    model=model,
    system_prompt="""You are a food ordering assistant.
          Your job is to:
          - Recommend food based on user preferences
          - Filter food by budget, calories, and preferences
          - Create food orders when requested
          - Use tools to provide accurate results
         Respond in the same language the user is using.""",
    model_settings=ModelSettings(temperature=0.3)
)

agent.tool_plain(recommend_food)
agent.tool_plain(reserve_food)
