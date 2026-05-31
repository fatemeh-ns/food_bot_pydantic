import os
import time
import asyncio
import warnings
# from typing import Optional
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.tools.recommend_tool import recommend_food
from app.tools.reserve_tool import reserve_food

warnings.filterwarnings("ignore")
load_dotenv()

model = OpenAIChatModel(
    "gpt-4o-mini",
    provider=OpenAIProvider(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
)

SYSTEM_PROMPT = """You are a food ordering assistant.
- Recommend food based on user preferences
- Filter food by budget, calories, and preferences
- Create food orders when requested
- Use tools to provide accurate results
Respond in the same language the user is using."""

# ─────
agent_with_tools = Agent(model=model, system_prompt=SYSTEM_PROMPT)
agent_with_tools.tool_plain(recommend_food)
agent_with_tools.tool_plain(reserve_food)

agent_no_tools = Agent(model=model, system_prompt=SYSTEM_PROMPT)

# ──────
TEST_INPUT = "غذای گیاهی میخوام، بودجه‌ام ۲۵۰ هزار تومنه"

NUM_RUNS = 5


async def run_benchmark(agent, label: str):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")

    latencies = []

    for i in range(NUM_RUNS):
        start = time.time()
        result = await agent.run(TEST_INPUT)
        elapsed = round(time.time() - start, 2)
        latencies.append(elapsed)

        answer = str(result.output)[:80].replace("\n", " ")
        print(f"  Run {i+1}: {elapsed}s  →  {answer}...")

    avg = round(sum(latencies) / len(latencies), 2)
    mn = round(min(latencies), 2)
    mx = round(max(latencies), 2)

    print(f"\nمیانگین : {avg}s")
    print(f"کمترین  : {mn}s")
    print(f"بیشترین : {mx}s")

    return {"label": label, "avg": avg, "min": mn, "max": mx}


async def main():
    print("\nشروع بنچمارک PydanticAI Food Agent")
    print(f"   تسک: {TEST_INPUT}")
    print(f"   تعداد اجرا: {NUM_RUNS}")

    r1 = await run_benchmark(agent_with_tools, "با Tool Calling")
    r2 = await run_benchmark(agent_no_tools,   "بدون Tool Calling")

    print(f"\n{'='*55}")
    print("نتیجه نهایی مقایسه")
    print(f"{'='*55}")
    print(f"  با Tool    → میانگین: {r1['avg']}s")
    print(f"  بدون Tool  → میانگین: {r2['avg']}s")
    diff = round(r1['avg'] - r2['avg'], 2)
    if diff > 0:
        print(f"\nTool calling  {diff}s کندتر بود (به خاطر اجرای tool)")
    else:
        print(f"\nبدون tool  {abs(diff)}s کندتر بود")


if __name__ == "__main__":
    asyncio.run(main())
