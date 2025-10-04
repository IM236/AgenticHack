"""GPT-5 client wrapper for the agents."""
from typing import Any, Dict
from openai import OpenAI
from pydantic import BaseModel
import json
import asyncio


class GPT5Client:
    """Wrapper for GPT-5 API that mimics LangChain interface."""

    def __init__(self, api_key: str, model: str = "gpt-5", temperature: float = 0.3):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def with_structured_output(self, schema: type[BaseModel]):
        """Return a client that extracts structured output."""
        return StructuredGPT5Client(
            client=self.client,
            model=self.model,
            temperature=self.temperature,
            schema=schema
        )

    async def ainvoke(self, messages: list) -> str:
        """Invoke GPT-5 with messages (async)."""
        # Convert messages to single input string
        input_text = self._messages_to_input(messages)

        # Run in thread pool since OpenAI client is synchronous
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.responses.create(
                model=self.model,
                input=input_text
            )
        )

        return response.output_text

    def _messages_to_input(self, messages: list) -> str:
        """Convert LangChain-style messages to GPT-5 input."""
        parts = []
        for msg in messages:
            if hasattr(msg, 'type'):
                if msg.type == 'system':
                    parts.append(f"System: {msg.content}")
                elif msg.type == 'human':
                    parts.append(f"User: {msg.content}")
            else:
                parts.append(str(msg))
        return "\n\n".join(parts)


class StructuredGPT5Client:
    """GPT-5 client that extracts structured output."""

    def __init__(self, client: OpenAI, model: str, temperature: float, schema: type[BaseModel]):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.schema = schema

    async def ainvoke(self, messages: list) -> BaseModel:
        """Invoke GPT-5 and extract structured output."""
        # Convert messages to input
        input_text = self._messages_to_input(messages)

        # Add schema instructions
        schema_json = self.schema.model_json_schema()
        input_with_schema = f"""{input_text}

You must respond ONLY with valid JSON matching this schema:
{json.dumps(schema_json, indent=2)}

Respond with valid JSON only, no other text."""

        # Run in thread pool since OpenAI client is synchronous
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.responses.create(
                model=self.model,
                input=input_with_schema
            )
        )

        # Parse JSON response
        output = response.output_text.strip()

        # Extract JSON if wrapped in markdown
        if output.startswith("```json"):
            output = output[7:]
        if output.endswith("```"):
            output = output[:-3]
        output = output.strip()

        # Parse and validate
        data = json.loads(output)
        return self.schema(**data)

    def _messages_to_input(self, messages: list) -> str:
        """Convert LangChain-style messages to GPT-5 input."""
        parts = []
        for msg in messages:
            if hasattr(msg, 'type'):
                if msg.type == 'system':
                    parts.append(f"System: {msg.content}")
                elif msg.type == 'human':
                    parts.append(f"User: {msg.content}")
            else:
                parts.append(str(msg))
        return "\n\n".join(parts)
