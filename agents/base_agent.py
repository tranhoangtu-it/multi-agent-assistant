"""Base agent class — all specialized agents inherit from this."""

import os
from typing import Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class BaseAgent:
    """Minimal async OpenAI agent. Subclasses set name, role, and instructions.

    Pass a pre-built ``client`` for testing (avoids requiring a real API key).
    """

    def __init__(
        self,
        name: str,
        role: str,
        instructions: str,
        client: Optional[AsyncOpenAI] = None,
    ) -> None:
        self.name = name
        self.role = role
        self.instructions = instructions
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        # Allow injecting a mock client for tests; otherwise build from env key.
        self._client: AsyncOpenAI = client or AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    async def run(self, task: str, context: str = "") -> str:
        """
        Call the chat completion API and return the assistant's reply as a string.

        Args:
            task:    The primary task description.
            context: Optional output from a previous agent to build on.
        """
        system_prompt = f"You are a {self.role}.\n\n{self.instructions}"
        user_message = task if not context else f"{task}\n\n--- Prior context ---\n{context}"

        try:
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            return f"[{self.name} error]: {exc}"
