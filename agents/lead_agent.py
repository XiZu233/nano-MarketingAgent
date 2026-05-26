from __future__ import annotations

from pathlib import Path

import pandas as pd

from agents.base import AgentBase
from providers.base import BaseLLMProvider
from schemas import LeadRecord


class LeadAgent(AgentBase):
    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider, "skills/lead_agent.md")

    def run(self, keyword: str, output_dir: Path, max_leads: int = 50) -> pd.DataFrame:
        output_dir.mkdir(parents=True, exist_ok=True)
        records = self._mock_comments(keyword)
        filtered = self._filter_and_dedupe(records)[:max_leads]
        df = pd.DataFrame([record.model_dump() for record in filtered])
        df.to_csv(output_dir / "leads.csv", index=False, encoding="utf-8-sig")
        return df

    def _filter_and_dedupe(self, records: list[LeadRecord]) -> list[LeadRecord]:
        best_by_user: dict[str, LeadRecord] = {}
        for record in records:
            if record.intent_score < 4:
                continue
            current = best_by_user.get(record.username)
            if current is None or record.intent_score > current.intent_score:
                best_by_user[record.username] = record
        return sorted(best_by_user.values(), key=lambda item: item.intent_score, reverse=True)

    def _mock_comments(self, keyword: str) -> list[LeadRecord]:
        source = f"{keyword} 高互动笔记"
        rows = [
            ("山城小面包", "求地址！明天想带朋友去", 5, "明确近期行动"),
            ("火锅脑袋77", "今晚营业到几点？想下班冲", 5, "明确近期行动并询问营业时间"),
            ("周末想出门", "这周末去要预约吗？两个人", 5, "明确周末到店意向"),
            ("辣度刚刚好", "有没有团购？明天中午想去", 5, "明确时间且询问优惠"),
            ("观音桥打工人", "离观音桥地铁站远不远？今晚想吃", 5, "明确今晚消费意向"),
            ("认真吃饭中", "人均大概多少呀？", 4, "询问价格信息"),
            ("不想排队", "排队久吗，周五晚上去会不会等很久", 4, "询问排队情况"),
            ("奶茶配火锅", "有微辣吗？朋友不能吃太辣", 4, "询问产品适配信息"),
            ("收藏夹满了", "具体在哪条路呀", 4, "询问地址信息"),
            ("南坪小王", "营业到凌晨吗？想夜宵去", 4, "询问营业时间"),
            ("甜辣都要", "看起来好好吃，收藏了", 3, "强烈兴趣但没有明确行动"),
            ("今天也饿了", "码住，下次去重庆试试", 3, "收藏型兴趣"),
            ("喜欢牛油锅", "这个锅底看着好香", 3, "表达兴趣"),
            ("路过看看", "不错", 2, "弱兴趣"),
            ("随手一评", "mark", 2, "弱兴趣"),
        ]
        return [
            LeadRecord(
                username=username,
                comment=comment,
                intent_score=score,
                source_note=source,
                reason=reason,
            )
            for username, comment, score, reason in rows
        ]
