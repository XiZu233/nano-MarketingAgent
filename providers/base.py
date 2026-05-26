from __future__ import annotations

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """统一模型 Provider 接口，Agent 只依赖这个抽象。"""

    name: str = "base"

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, **kwargs: object) -> str:
        """生成文本。具体 Provider 可接小浣熊、OpenAI 或其他模型。"""
