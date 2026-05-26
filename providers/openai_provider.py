from __future__ import annotations

import os

from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    name = "openai"

    def generate(self, system_prompt: str, user_prompt: str, **kwargs: object) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("未配置 OPENAI_API_KEY，无法使用 OpenAI Provider。")
        raise NotImplementedError("OpenAI Provider 已预留接口，当前 MVP 默认使用 mock provider。")
