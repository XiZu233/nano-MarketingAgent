from __future__ import annotations

import os

from .base import BaseLLMProvider


class XiaohuanxiongProvider(BaseLLMProvider):
    name = "xiaohuanxiong"

    def generate(self, system_prompt: str, user_prompt: str, **kwargs: object) -> str:
        endpoint = os.getenv("XIAOHUANXIONG_ENDPOINT")
        api_key = os.getenv("XIAOHUANXIONG_API_KEY")
        if not endpoint or not api_key:
            raise RuntimeError("未配置 XIAOHUANXIONG_ENDPOINT 或 XIAOHUANXIONG_API_KEY。")
        raise NotImplementedError("小浣熊 Provider 已预留接口，拿到正式 API 后补齐请求实现。")
