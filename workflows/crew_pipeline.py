from __future__ import annotations

from workflows.pipeline import run_pipeline


def run_crew_pipeline(*args: object, **kwargs: object) -> object:
    """CrewAI 增强模式占位。

    当前 MVP 使用稳定的原生 Python pipeline。后续接入 CrewAI 时，
    这里继续复用现有 Agent 业务逻辑，避免重复实现。
    """

    raise NotImplementedError("CrewAI 模式已预留，当前请使用 workflows.pipeline.run_pipeline。")


__all__ = ["run_crew_pipeline", "run_pipeline"]
