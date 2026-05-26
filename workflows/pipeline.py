from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents import CopyAgent, LeadAgent, OutreachAgent, SEOAgent
from providers import get_provider
from schemas import ContentPiece, MerchantInfo, OutreachMessage, SEOReport
from tools import package_outputs


@dataclass
class PipelineResult:
    run_id: str
    output_dir: Path
    seo_report: SEOReport
    leads: pd.DataFrame
    content: list[ContentPiece]
    outreach: list[OutreachMessage]
    zip_path: Path
    timings: dict[str, float]


def build_run_id(merchant_name: str) -> str:
    safe_name = "".join(ch for ch in merchant_name if ch.isalnum() or ch in ("-", "_")) or "merchant"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{safe_name}"


def run_pipeline(
    industry: str,
    merchant_info: MerchantInfo | dict[str, object],
    keyword: str | None = None,
    run_id: str | None = None,
    outputs_root: str | Path = "outputs",
) -> PipelineResult:
    merchant = merchant_info if isinstance(merchant_info, MerchantInfo) else MerchantInfo(**merchant_info)
    keyword = keyword or f"{industry}推荐"
    provider = get_provider()
    run_id = run_id or build_run_id(merchant.name)
    output_dir = Path(outputs_root) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    timings: dict[str, float] = {}

    seo_agent = SEOAgent(provider)
    lead_agent = LeadAgent(provider)
    copy_agent = CopyAgent(provider)
    outreach_agent = OutreachAgent(provider)

    print(f"[RUN] run_id={run_id} provider={provider.name}")
    with ThreadPoolExecutor(max_workers=2) as executor:
        seo_future = executor.submit(_timed, "SEO Agent", timings, seo_agent.run, industry, output_dir)
        lead_future = executor.submit(_timed, "Lead Agent", timings, lead_agent.run, keyword, output_dir)
        seo_report = seo_future.result()
        leads = lead_future.result()

    content = _timed("Copy Agent", timings, copy_agent.run, seo_report, merchant, output_dir)
    outreach = _timed("Outreach Agent", timings, outreach_agent.run, leads, merchant, output_dir)
    zip_path = _timed("Package", timings, package_outputs, output_dir)

    print(f"[DONE] 输出目录: {output_dir}")
    print(f"[DONE] 营销包: {zip_path}")
    for name, seconds in timings.items():
        print(f"[TIME] {name}: {seconds:.2f}s")

    return PipelineResult(
        run_id=run_id,
        output_dir=output_dir,
        seo_report=seo_report,
        leads=leads,
        content=content,
        outreach=outreach,
        zip_path=zip_path,
        timings=timings,
    )


def _timed(name: str, timings: dict[str, float], func: object, *args: object) -> object:
    start = time.perf_counter()
    print(f"[START] {name}")
    try:
        result = func(*args)
    except Exception as exc:
        print(f"[ERROR] {name}: {exc}")
        raise
    finally:
        timings[name] = time.perf_counter() - start
    print(f"[FINISH] {name}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="运行 NanoMarketing Engine 稳定模式流水线")
    parser.add_argument("--industry", default="重庆火锅")
    parser.add_argument("--merchant-name", default="老灶门")
    parser.add_argument("--selling-points", default="牛油现炒,毛肚新鲜,社区老店")
    parser.add_argument("--address", default="观音桥XX路")
    parser.add_argument("--price-per-person", type=int, default=60)
    parser.add_argument("--special-offer", default="小红书送冰粉")
    args = parser.parse_args()

    merchant = MerchantInfo(
        name=args.merchant_name,
        industry=args.industry,
        selling_points=[item.strip() for item in args.selling_points.split(",") if item.strip()],
        address=args.address,
        price_per_person=args.price_per_person,
        special_offer=args.special_offer,
    )
    run_pipeline(args.industry, merchant)


if __name__ == "__main__":
    main()
