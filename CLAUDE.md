# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install dependencies: `pip install -r requirements.txt`
- Run the interactive food-ordering agent: `python -m app.main`
- Run the PydanticAI benchmark comparing tool-calling vs no-tool agents: `python benchmark_pydantic.py`
- Quick syntax/import check: `python -m compileall app benchmark_pydantic.py`

There is currently no test suite, lint configuration, or build step in this repository. The app and benchmark require a `.env` file with `OPENROUTER_API_KEY` for OpenRouter access.

## Architecture

This is a small PydanticAI-based CLI food-ordering assistant backed by SQLite.

- `app/main.py` is the interactive CLI entry point. It keeps `chat_history` in memory and passes it to `agent.run(...)` on each user turn.
- `app/agent.py` constructs the production `pydantic_ai.Agent`. It loads environment variables with `python-dotenv`, configures an `OpenAIChatModel` named `gpt-4o-mini` through OpenRouter (`https://openrouter.ai/api/v1`), sets the food-assistant system prompt, and registers tools with `agent.tool_plain(...)`.
- `app/tools/recommend_tool.py` and `app/tools/reserve_tool.py` are plain Python functions exposed as PydanticAI tools. They return JSON strings rather than Python objects.
  - `recommend_food(...)` queries the `foods` table and supports filtering by maximum price, vegetarian flag, and spicy flag.
  - `reserve_food(...)` inserts a pending order into the `orders` table and appends a JSON-line audit record to `orders.log`.
- `app/db.py` centralizes SQLite connection creation. Connections point to relative path `food.db`, so commands should be run from the repository root unless this is changed.
- `benchmark_pydantic.py` duplicates the model setup and system prompt to compare a PydanticAI agent with registered tools against an agent without tools for a fixed Persian-language prompt. It stores per-run and average results in `logs/benchmark_results.db`.

## Data model and local files

The checked-in workflow expects a local SQLite database named `food.db` with these tables:

- `foods(id, name, category, price, calories, spicy, vegetarian)`
- `orders(id, food_id, user_name, status, created_at)`

Runtime-local files are intentionally ignored by git: `.env`, `*.db`, `*.log`, and `__pycache__/`. Do not assume `food.db` or `orders.log` exists in a fresh clone; create or seed the database before running tool-backed flows if needed.
