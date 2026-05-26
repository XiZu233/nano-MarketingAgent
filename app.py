from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from schemas import MerchantInfo
from workflows import run_pipeline


st.set_page_config(page_title="NanoMarketing Engine", page_icon="N", layout="wide")

st.title("NanoMarketing Engine")
st.caption("四 Agent 本地生活营销流水线：SEO 分析、线索挖掘、文案生成、触达话术。")

with st.sidebar:
    st.header("商家信息")
    industry = st.selectbox("行业", ["重庆火锅", "餐饮", "美业", "教培", "健身"], index=0)
    merchant_name = st.text_input("商家名称", value="老灶门")
    selling_points_text = st.text_area("卖点，逗号分隔", value="牛油现炒, 毛肚新鲜, 社区老店")
    address = st.text_input("地址", value="观音桥XX路")
    price_per_person = st.number_input("人均消费", min_value=1, max_value=9999, value=60, step=1)
    special_offer = st.text_input("暗号福利", value="小红书送冰粉")
    run_mode = st.radio("运行模式", ["稳定模式", "CrewAI 模式"], horizontal=True)
    submitted = st.button("开始生成", type="primary", use_container_width=True)

selling_points = [item.strip() for item in selling_points_text.split(",") if item.strip()]
if not selling_points:
    selling_points = ["招牌产品稳定"]

st.info("系统就绪。填写左侧表单后点击开始生成。", icon="ℹ️")

if submitted:
    if run_mode == "CrewAI 模式":
        st.warning("CrewAI 模式已预留，当前 MVP 自动切回稳定模式。")

    merchant = MerchantInfo(
        name=merchant_name,
        industry=industry,
        selling_points=selling_points,
        address=address,
        price_per_person=int(price_per_person),
        special_offer=special_offer,
    )

    progress = st.progress(0)
    status_area = st.empty()
    status_area.write("SEO Agent 与 Lead Agent 并行启动中...")
    progress.progress(20)

    try:
        result = run_pipeline(industry=industry, merchant_info=merchant)
    except Exception as exc:
        st.error(f"流水线执行失败: {exc}")
        st.stop()

    progress.progress(100)
    status_area.success(f"四 Agent 已完成，输出目录：{result.output_dir}")

    tab_seo, tab_content, tab_leads, tab_outreach = st.tabs(["SEO 报告", "文案包", "线索表", "话术库"])

    with tab_seo:
        st.json(result.seo_report.model_dump())

    with tab_content:
        for index, piece in enumerate(result.content, start=1):
            with st.container(border=True):
                st.subheader(f"文案 {index}: {piece.title}")
                st.write(piece.body)
                st.code(piece.image_prompt, language="text")
                st.write(" ".join(f"#{tag}" for tag in piece.hashtags))
        st.download_button(
            "下载 content_package.json",
            data=json.dumps([item.model_dump() for item in result.content], ensure_ascii=False, indent=2),
            file_name="content_package.json",
            mime="application/json",
        )

    with tab_leads:
        st.dataframe(result.leads, use_container_width=True)
        st.download_button(
            "下载 leads.csv",
            data=result.leads.to_csv(index=False).encode("utf-8-sig"),
            file_name="leads.csv",
            mime="text/csv",
        )

    with tab_outreach:
        outreach_path = Path(result.output_dir) / "outreach_kit.md"
        outreach_text = outreach_path.read_text(encoding="utf-8")
        st.markdown(outreach_text)
        st.download_button(
            "下载 outreach_kit.md",
            data=outreach_text.encode("utf-8"),
            file_name="outreach_kit.md",
            mime="text/markdown",
        )

    zip_bytes = Path(result.zip_path).read_bytes()
    st.download_button(
        "下载完整营销包",
        data=zip_bytes,
        file_name="marketing_package.zip",
        mime="application/zip",
        type="primary",
    )
