from __future__ import annotations

import json
from pathlib import Path

from agents.base import AgentBase
from providers.base import BaseLLMProvider
from schemas import ContentPiece, MerchantInfo, SEOReport


class CopyAgent(AgentBase):
    def __init__(self, provider: BaseLLMProvider) -> None:
        super().__init__(provider, "skills/copy_agent.md")

    def run(self, seo_report: SEOReport, merchant_info: MerchantInfo, output_dir: Path) -> list[ContentPiece]:
        output_dir.mkdir(parents=True, exist_ok=True)
        pieces = [self._build_piece(index, formula, seo_report, merchant_info) for index, formula in enumerate(seo_report.title_formulas[:3])]
        output_path = output_dir / "content_package.json"
        output_path.write_text(
            json.dumps([piece.model_dump() for piece in pieces], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return pieces

    def _build_piece(
        self,
        index: int,
        formula: str,
        seo_report: SEOReport,
        merchant: MerchantInfo,
    ) -> ContentPiece:
        location = self._short_location(merchant.address)
        category = merchant.industry
        emotion = ["绝了", "宝藏", "私藏"][index % 3]
        adjective = ["香迷糊", "上头", "值得冲"][index % 3]
        title = (
            formula.replace("{情绪词}", emotion)
            .replace("{地点}", location)
            .replace("{品类}", category)
            .replace("{形容词}", adjective)
            .replace("{数字}", str(index + 3))
            .replace("{人群标签}", "本地人")
        )
        selling_points = merchant.selling_points
        first_point = selling_points[0]
        second_point = selling_points[1] if len(selling_points) > 1 else selling_points[0]
        third_point = selling_points[2] if len(selling_points) > 2 else first_point
        bodies = [
            (
                f"下班路过{location}的时候，我又被{merchant.name}香到停住脚。"
                f"这家最戳我的是{first_point}，入口是很踏实的香，不是那种只会冲鼻子的味道。"
                f"{second_point}也很在线，朋友夹第一口就开始点头，配菜煮久了也不寡。"
                f"人均大概{merchant.price_per_person}元，想吃得舒服建议早点去，晚高峰可能要排队。"
                f"地址在{merchant.address}，约朋友吃饭可以直接把这篇甩给他。"
            ),
            (
                f"如果你最近想找一家不踩雷的{category}，我会把{merchant.name}放进清单。"
                f"{first_point}是它的记忆点，{second_point}让整顿饭很有满足感。"
                f"我还挺喜欢{third_point}，不是硬凹网红感，是真的适合认真吃一顿。"
                f"人均{merchant.price_per_person}元左右，周末建议提前问下排队情况。"
                f"店在{merchant.address}，想吃热闹一点的局可以安排。"
            ),
            (
                f"本地朋友带我去{merchant.name}之后，我懂为什么它会被反复安利了。"
                f"{first_point}吃起来很有辨识度，{second_point}也不是摆样子。"
                f"整家店的感觉很适合朋友小聚，边吃边聊会不知不觉加菜。"
                f"人均大约{merchant.price_per_person}元，饭点去记得留点排队时间。"
                f"位置在{merchant.address}，收藏起来，下次不知道吃什么就冲这里。"
            ),
        ]
        hashtag_set = seo_report.hashtag_sets[index % len(seo_report.hashtag_sets)]
        image_prompt = (
            f"小红书探店封面，{merchant.name}，{category}，{seo_report.cover_rules.style}，"
            f"{seo_report.cover_rules.ratio}，突出{first_point}，标题大字清晰"
        )
        return ContentPiece(
            title=title,
            body=bodies[index],
            image_prompt=image_prompt,
            hashtags=hashtag_set,
        )

    def _short_location(self, address: str) -> str:
        for keyword in ["观音桥", "解放碑", "南坪", "沙坪坝", "江北", "渝中"]:
            if keyword in address:
                return keyword
        return address[:6] if address else "附近"
