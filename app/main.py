import asyncio
from app.agent import agent
# from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart


async def chat():
    print("Food Agent is running... (type 'exit' to quit)")
    chat_history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        result = await agent.run(user_input, message_history=chat_history)

        answer = result.output
        print("Agent:", answer)

        chat_history += result.new_messages()


if __name__ == "__main__":
    asyncio.run(chat())
