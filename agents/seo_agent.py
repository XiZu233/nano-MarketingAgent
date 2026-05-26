from __future__ import annotations

import json
from pathlib import Path

from agents.base import AgentBase
from providers.base import BaseLLMProvider
from schemas import CoverRules, SEOReport


class SEOAgent(AgentBase):
    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider, "skills/seo_agent.md")

    def run(self, industry: str, output_dir: Path) -> SEOReport:
        output_dir.mkdir(parents=True, exist_ok=True)
        report = self._mock_report(industry)
        output_path = output_dir / "seo_report.json"
        output_path.write_text(
            json.dumps(report.model_dump(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return report

    def _mock_report(self, industry: str) -> SEOReport:
        if industry == "重庆火锅":
            return SEOReport(
                industry=industry,
                title_formulas=[
                    "{情绪词}！{地点}这家{品类}真的{形容词}",
                    "{数字}家{地点}必吃{品类}，第{数字}家绝了",
                    "{人群标签}私藏！{地点}{品类}天花板",
                ],
                keywords={
                    "location": ["观音桥", "解放碑", "南坪"],
                    "category": ["重庆火锅", "老火锅", "社区火锅"],
                    "emotion": ["绝了", "宝藏", "私藏", "排队也要吃"],
                },
                cover_rules=CoverRules(
                    ratio="3:4",
                    style="暖色调+大字报+人物半身+食物特写",
                    text_size="标题字号占画面 1/5",
                    color_scheme="红/橙/黄为主，黑字白边",
                ),
                posting_time="18:00-20:00 或 11:00-13:00",
                hashtag_sets=[
                    ["重庆火锅", "本地人推荐", "美食探店"],
                    ["藏在巷子里的美食", "重庆旅游", "火锅约起来"],
                ],
            )

        category = industry or "本地生活"
        return SEOReport(
            industry=category,
            title_formulas=[
                "{情绪词}！{地点}这家{品类}真的{形容词}",
                "{数字}家{地点}必打卡{品类}，第{数字}家很惊喜",
                "{人群标签}私藏！{地点}{品类}体验感拉满",
            ],
            keywords={
                "location": ["商圈附近", "社区周边", "地铁口"],
                "category": [category, f"{category}推荐", f"{category}探店"],
                "emotion": ["宝藏", "舒服", "值得冲", "很惊喜"],
            },
            cover_rules=CoverRules(
                ratio="3:4",
                style="明亮自然光+主体特写+清晰标题",
                text_size="标题字号占画面 1/5",
                color_scheme="高对比暖色标题，背景保持干净",
            ),
            posting_time="18:00-20:00 或 12:00-13:30",
            hashtag_sets=[
                [category, "本地人推荐", "周末去哪儿"],
                ["宝藏小店", "同城生活", "探店分享"],
            ],
        )
