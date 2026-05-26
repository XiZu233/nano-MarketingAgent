from __future__ import annotations

from pathlib import Path

from agents import LeadAgent, OutreachAgent, SEOAgent
from providers.mock_provider import MockProvider
from schemas import MerchantInfo
from workflows import run_pipeline


def test_seo_report_has_required_formulas(tmp_path: Path) -> None:
    report = SEOAgent(MockProvider()).run("重庆火锅", tmp_path)

    assert len(report.title_formulas) >= 3
    assert all("{" in formula and "}" in formula for formula in report.title_formulas)


def test_lead_agent_filters_low_intent(tmp_path: Path) -> None:
    leads = LeadAgent(MockProvider()).run("重庆火锅推荐", tmp_path)

    assert len(leads) >= 10
    assert set(["username", "comment", "intent_score", "source_note", "reason"]).issubset(leads.columns)
    assert (leads["intent_score"] >= 4).all()


def test_outreach_messages_are_short(tmp_path: Path) -> None:
    provider = MockProvider()
    leads = LeadAgent(provider).run("重庆火锅推荐", tmp_path)
    merchant = MerchantInfo(
        name="老灶门",
        industry="重庆火锅",
        selling_points=["牛油现炒", "毛肚新鲜"],
        address="观音桥XX路",
        price_per_person=60,
        special_offer="小红书送冰粉",
    )

    messages = OutreachAgent(provider).run(leads, merchant, tmp_path)

    assert messages
    assert all(len(item.message) <= 120 for item in messages)


def test_full_pipeline_outputs_package(tmp_path: Path) -> None:
    merchant = MerchantInfo(
        name="老灶门",
        industry="重庆火锅",
        selling_points=["牛油现炒", "毛肚新鲜", "社区老店"],
        address="观音桥XX路",
        price_per_person=60,
        special_offer="小红书送冰粉",
    )

    result = run_pipeline("重庆火锅", merchant, run_id="test_run", outputs_root=tmp_path)

    assert (result.output_dir / "seo_report.json").exists()
    assert (result.output_dir / "leads.csv").exists()
    assert (result.output_dir / "content_package.json").exists()
    assert (result.output_dir / "outreach_kit.md").exists()
    assert result.zip_path.exists()
