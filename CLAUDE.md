# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

This is a Python project using pydantic-ai for building AI agents. The project
uses the modern Python package manager `uv` for dependency management and
requires Python 3.13+.

## Development Commands

- **Install dependencies**: `uv sync`
- **Run the main example**: `uv run python main.py`
- **Run the hello world agent**: `uv run python hello_world.py`
- **Run the chat agent**: `uv run python chat_agent.py`
- **Start OpenAI compatibility server**: `uv run python openai_compat.py`
- **Test OpenAI compatibility**: `uv run python test_openai_compat.py`
- **Add new dependencies**: `uv add <package>`

## Architecture

The project demonstrates various pydantic-ai usage patterns and includes an
OpenAI API compatibility layer:

### Core Components

- `hello_world.py`: Simple agent example using Google's Gemini model with a
basic system prompt
- `chat_agent.py`: Interactive command-line conversational agent with chat loop
- `openai_compat.py`: FastAPI-based OpenAI API compatibility layer that
translates OpenAI requests to pydantic-ai calls
- `test_openai_compat.py`: Test suite for the OpenAI compatibility layer

### OpenAI Compatibility Layer

The `openai_compat.py` file provides a FastAPI server that implements
OpenAI-compatible endpoints:

- **Endpoints**: `/v1/chat/completions`, `/v1/models`
- **Features**: Streaming responses, token usage estimation, proper error
handling
- **Translation**: Converts OpenAI message format to pydantic-ai conversation
strings
- **Async Support**: Uses `await agent.run()` to avoid event loop conflicts

The compatibility layer allows existing OpenAI client libraries to work with
pydantic-ai agents by pointing them to `http://localhost:8000`.

All agents use Google's Gemini 1.5 Flash model (`google-gla:gemini-1.5-flash`)
as the LLM backend.

## Key Dependencies

- **pydantic-ai[logfire]**: The main framework for building AI agents with
Pydantic integration and Logfire logging support
- **fastapi**: Web framework for the OpenAI compatibility API server
- **uvicorn**: ASGI server for running the FastAPI application
- **requests**: HTTP client library for testing the compatibility layer
