from __future__ import annotations

from pathlib import Path

from providers.base import BaseLLMProvider


class AgentBase:
    def __init__(self, provider: BaseLLMProvider, skill_path: str) -> None:
        self.provider = provider
        self.skill_path = Path(skill_path)
        self.system_prompt = self._load_skill()

    def _load_skill(self) -> str:
        if not self.skill_path.exists():
            raise FileNotFoundError(f"角色卡不存在: {self.skill_path}")
        return self.skill_path.read_text(encoding="utf-8")
