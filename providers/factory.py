from __future__ import annotations

import os

from dotenv import load_dotenv

from .base import BaseLLMProvider
from .mock_provider import MockProvider
from .openai_provider import OpenAIProvider
from .xiaohuanxiong_provider import XiaohuanxiongProvider


def get_provider() -> BaseLLMProvider:
    load_dotenv()
    provider_name = os.getenv("MODEL_PROVIDER", "mock").strip().lower()
    providers: dict[str, type[BaseLLMProvider]] = {
        "mock": MockProvider,
        "openai": OpenAIProvider,
        "xiaohuanxiong": XiaohuanxiongProvider,
    }
    provider_cls = providers.get(provider_name)
    if provider_cls is None:
        raise ValueError(f"不支持的 MODEL_PROVIDER: {provider_name}")
    return provider_cls()
