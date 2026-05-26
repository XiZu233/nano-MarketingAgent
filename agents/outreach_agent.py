from __future__ import annotations

from pathlib import Path

import pandas as pd

from agents.base import AgentBase
from providers.base import BaseLLMProvider
from schemas import MerchantInfo, OutreachMessage


class OutreachAgent(AgentBase):
    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider, "skills/outreach_agent.md")

    def run(self, leads_df: pd.DataFrame, merchant_info: MerchantInfo, output_dir: Path) -> list[OutreachMessage]:
        output_dir.mkdir(parents=True, exist_ok=True)
        messages: list[OutreachMessage] = []
        seen: set[str] = set()
        for row in leads_df.to_dict(orient="records"):
            username = str(row["username"])
            if username in seen or int(row["intent_score"]) < 4:
                continue
            seen.add(username)
            message = self._build_message(str(row["comment"]), merchant_info)
            messages.append(
                OutreachMessage(
                    username=username,
                    original_comment=str(row["comment"]),
                    message=message,
                    send_timing="即时" if int(row["intent_score"]) == 5 else "当天饭点前",
                )
            )

        markdown = self._to_markdown(messages)
        (output_dir / "outreach_kit.md").write_text(markdown, encoding="utf-8")
        return messages

    def _build_message(self, comment: str, merchant: MerchantInfo) -> str:
        first_point = merchant.selling_points[0]
        if "地址" in comment or "哪" in comment or "远不远" in comment:
            core = f"宝子，就在{merchant.address}，人均{merchant.price_per_person}左右，{first_point}挺稳。"
        elif "人均" in comment or "多少" in comment or "团购" in comment:
            core = f"姐妹，人均大概{merchant.price_per_person}，{first_point}是亮点，性价比还可以。"
        elif "排队" in comment or "预约" in comment:
            core = f"友友，饭点可能要等，早点去更舒服，{first_point}确实值得排一下。"
        elif "营业" in comment or "夜宵" in comment:
            core = f"宝子，建议去前问下当天营业时间，{merchant.address}这家夜宵局很合适。"
        else:
            core = f"宝子，看来你也被种草了，{merchant.name}的{first_point}确实蛮香。"
        offer = f"这周报暗号“{merchant.special_offer}”有福利。"
        question = "你一般几点去？我帮你看看怎么避开排队。"
        return self._trim(f"{core}{offer}{question}", 120)

    def _trim(self, text: str, limit: int) -> str:
        return text if len(text) <= limit else text[: limit - 1] + "…"

    def _to_markdown(self, messages: list[OutreachMessage]) -> str:
        lines = ["| 用户名 | 原评论 | 回复话术 | 发送时机 |", "|---|---|---|---|"]
        for item in messages:
            lines.append(
                f"| {item.username} | {item.original_comment} | {item.message} | {item.send_timing} |"
            )
        return "\n".join(lines) + "\n"
