# NanoMarketing Engine

面向本地生活 Marketing 团队的四 Agent 营销流水线 MVP。输入行业和商家信息，系统会生成 SEO 爆款结构分析、3 篇小红书文案、高意向线索表、个性化触达话术，并打包为完整营销包。

## 工作流

```text
SEO Agent + Lead Agent 并行
        |
        +--> Copy Agent 依赖 SEO 报告生成文案
        |
        +--> Outreach Agent 依赖线索表生成话术
        |
        +--> marketing_package.zip
```

## 当前能力

- 稳定模式：原生 Python pipeline，不依赖外部网络。
- Mock 数据：适合比赛 Demo、流程验证和前端演示。
- Provider 抽象：预留 `mock`、`openai`、`xiaohuanxiong` 三种模型 Provider。
- Streamlit 总控：支持表单输入、结果展示和 zip 下载。
- CrewAI 增强位：已预留 `workflows/crew_pipeline.py`，不会影响稳定模式。

## 参考与本地化改造

项目参考了 [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) 中多 Agent 应用的产品组织方式，重点借鉴 Sales Intelligence、Competitor Intelligence 和 AI Services Agency 这类“多阶段 Agent + 结构化交付物”的模板。

本项目没有直接复制其实现，而是面向中国本地生活营销场景做本地化改造：将 battle card、竞品分析、虚拟 agency 等模式转换为小红书爆款分析、线索挖掘、商家文案和私信触达工作流。详细改造路线见 [docs/awesome_llm_apps_localization.md](docs/awesome_llm_apps_localization.md)。

## 安装

```powershell
pip install -r requirements.txt
```

## 命令行运行

```powershell
python workflows/pipeline.py
```

运行完成后会在 `outputs/{run_id}/` 生成：

- `seo_report.json`
- `leads.csv`
- `content_package.json`
- `outreach_kit.md`
- `marketing_package.zip`

## 启动前端

```powershell
streamlit run app.py
```

在左侧输入商家信息，点击“开始生成”，即可在 4 个 Tab 中查看结果并下载完整营销包。

## 模型 Provider 配置

默认使用 mock provider，不需要密钥。

如需切换模型，在 `.env` 中配置：

```text
MODEL_PROVIDER=mock
```

预留值：

```text
MODEL_PROVIDER=openai
MODEL_PROVIDER=xiaohuanxiong
```

当前 MVP 不硬编码任何 API Key。小浣熊 Provider 等拿到正式 API 后，在 `providers/xiaohuanxiong_provider.py` 中补齐请求实现。

## 测试

```powershell
python -m pytest
```

测试覆盖：

- SEO 报告至少包含 3 个可套用标题公式。
- Lead Agent 只输出 `intent_score >= 4` 的线索。
- Outreach 话术不超过 120 字。
- 完整 pipeline 能生成 4 个核心文件和 zip 包。

## 真实数据说明

当前版本不直接爬取小红书，避免反爬和合规风险。生产版本建议通过以下方式接入数据：

- 商家手动导入评论 CSV。
- 合规第三方搜索或舆情 API。
- 企业内部 CRM 或飞书表格。

## 参赛展示建议

演示顺序：

1. 输入真实或 Demo 商家信息。
2. 展示四 Agent 依赖关系。
3. 运行稳定模式生成结果。
4. 查看 SEO 报告、文案包、线索表、话术库。
5. 下载 `marketing_package.zip`。
6. 说明 Provider 抽象支持后续接入小浣熊或其他模型。
