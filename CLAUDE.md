# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `uv` for Python package management:

- **Install dependencies**: `uv sync`
- **Run main chat agent**: `uv run python chat_agent.py`
- **Run OpenAI compatibility server**: `uv run python openai_compat.py`
- **Test OpenAI compatibility**: `uv run python test_openai_compat.py` (requires server running)
- **Run simple hello world**: `uv run python main.py`

## Architecture Overview

This is a pydantic-ai project with two main components:

1. **Chat Agent** (`chat_agent.py`): Interactive conversational agent using pydantic-ai with Google Gemini 1.5 Flash
   - Simple CLI chat interface with quit/exit commands
   - Uses pydantic-ai Agent with system prompt configuration

2. **OpenAI Compatibility Layer** (`openai_compat.py`): FastAPI server providing OpenAI-compatible API endpoints
   - Implements `/v1/chat/completions` endpoint with streaming support
   - Implements `/v1/models` endpoint
   - Converts OpenAI chat format to pydantic-ai format
   - Provides token usage estimation
   - Runs on port 8000 by default

### Key Dependencies
- **pydantic-ai[logfire]**: Core AI agent framework
- **FastAPI**: Web framework for API compatibility layer
- **uvicorn**: ASGI server for FastAPI
- **requests**: HTTP client (used in tests)

### Project Structure
- `chat_agent.py`: CLI chat interface
- `openai_compat.py`: OpenAI-compatible API server
- `test_openai_compat.py`: Manual testing script for API endpoints
- `main.py`: Simple hello world entry point
- `pyproject.toml`: Project configuration and dependencies