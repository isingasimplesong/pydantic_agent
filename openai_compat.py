#!/usr/bin/env python3

import json
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic_ai import Agent

app = FastAPI(title="OpenAI API Compatibility Layer", version="0.1.0")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatChoice]
    usage: ChatUsage


class ChatStreamChoice(BaseModel):
    index: int
    delta: Dict[str, Any]
    finish_reason: Optional[str] = None


class ChatStreamResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatStreamChoice]


# Initialize agent
agent = Agent(
    "google-gla:gemini-1.5-flash", system_prompt="You are a helpful AI assistant."
)


def build_conversation(messages: List[ChatMessage]) -> str:
    """Convert OpenAI messages format to a single prompt for pydantic-ai"""
    conversation_parts = []

    for message in messages:
        if message.role == "system":
            # System messages are handled by the agent's system_prompt
            continue
        elif message.role == "user":
            conversation_parts.append(f"User: {message.content}")
        elif message.role == "assistant":
            conversation_parts.append(f"Assistant: {message.content}")

    return "\n".join(conversation_parts)


def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 characters per token)"""
    return len(text) // 4


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    try:
        # Build conversation from messages
        conversation = build_conversation(request.messages)

        if request.stream:
            return StreamingResponse(
                stream_chat_response(conversation, request), media_type="text/plain"
            )
        else:
            # Run the agent asynchronously
            result = await agent.run(conversation)

            # Create response
            response_id = f"chatcmpl-{uuid.uuid4().hex[:29]}"

            # Estimate token usage
            prompt_tokens = estimate_tokens(conversation)
            completion_tokens = estimate_tokens(result.output)

            response = ChatResponse(
                id=response_id,
                object="chat.completion",
                created=int(time.time()),
                model=request.model,
                choices=[
                    ChatChoice(
                        index=0,
                        message=ChatMessage(role="assistant", content=result.output),
                        finish_reason="stop",
                    )
                ],
                usage=ChatUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                ),
            )

            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def stream_chat_response(conversation: str, request: ChatRequest):
    """Generate streaming response in OpenAI format"""
    try:
        response_id = f"chatcmpl-{uuid.uuid4().hex[:29]}"
        created = int(time.time())

        # For streaming, we'll simulate by running the agent and chunking the response
        result = await agent.run(conversation)
        content = result.output

        # Split content into chunks (simulate streaming)
        chunk_size = 10
        chunks = [
            content[i : i + chunk_size] for i in range(0, len(content), chunk_size)
        ]

        for chunk in enumerate(chunks):
            stream_response = ChatStreamResponse(
                id=response_id,
                object="chat.completion.chunk",
                created=created,
                model=request.model,
                choices=[
                    ChatStreamChoice(
                        index=0, delta={"content": chunk}, finish_reason=None
                    )
                ],
            )

            yield f"data: {stream_response.model_dump_json()}\n\n"

        # Send final chunk
        final_response = ChatStreamResponse(
            id=response_id,
            object="chat.completion.chunk",
            created=created,
            model=request.model,
            choices=[ChatStreamChoice(index=0, delta={}, finish_reason="stop")],
        )

        yield f"data: {final_response.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"

    except Exception as e:
        error_response = {"error": {"message": str(e), "type": "internal_error"}}
        yield f"data: {json.dumps(error_response)}\n\n"


@app.get("/v1/models")
async def list_models():
    """List available models"""
    return {
        "object": "list",
        "data": [
            {
                "id": "google-gla:gemini-1.5-flash",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "google",
            }
        ],
    }


@app.get("/")
async def root():
    return {"message": "OpenAI API Compatibility Layer for pydantic-ai"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
