from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class CoverRules(BaseModel):
    ratio: str
    style: str
    text_size: str
    color_scheme: str


class SEOReport(BaseModel):
    industry: str
    platform: str = "小红书"
    title_formulas: list[str] = Field(min_length=3)
    keywords: dict[str, list[str]]
    cover_rules: CoverRules
    posting_time: str
    hashtag_sets: list[list[str]]

    @field_validator("title_formulas")
    @classmethod
    def title_formulas_need_placeholders(cls, formulas: list[str]) -> list[str]:
        missing = [formula for formula in formulas if "{" not in formula or "}" not in formula]
        if missing:
            raise ValueError(f"标题公式缺少占位符: {missing}")
        return formulas


class LeadRecord(BaseModel):
    username: str
    comment: str
    intent_score: int = Field(ge=1, le=5)
    source_note: str
    reason: str


class MerchantInfo(BaseModel):
    name: str
    industry: str
    selling_points: list[str] = Field(min_length=1)
    address: str
    price_per_person: int = Field(gt=0)
    special_offer: str = "报小红书送小食"


class ContentPiece(BaseModel):
    title: str
    body: str
    image_prompt: str
    hashtags: list[str]


class OutreachMessage(BaseModel):
    username: str
    original_comment: str
    message: str = Field(max_length=120)
    send_timing: str = "即时"
