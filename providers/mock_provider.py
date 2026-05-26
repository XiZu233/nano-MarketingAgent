from __future__ import annotations

from .base import BaseLLMProvider


class MockProvider(BaseLLMProvider):
    name = "mock"

    def generate(self, system_prompt: str, user_prompt: str, **kwargs: object) -> str:
        return "MOCK_PROVIDER_OUTPUT"
