# 基于 awesome-llm-apps 的本地化改造方案

本文记录 NanoMarketing Engine 对 [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) 中多 Agent 应用案例的借鉴方式。目标不是复制代码，而是吸收其“可运行模板、结构化产物、多阶段 Agent、专业交付物”的产品设计方法，并改造成适合中国本地生活营销团队的工作流。

## 参考案例

### AI Sales Intelligence Agent Team

可借鉴点：
- 用多阶段流水线生成专业销售物料，而不是只返回聊天文本。
- 每个 Agent 都有明确的 `Output Key`，方便下游消费。
- 最终产物是 HTML battle card、比较图、话术脚本等可直接交付的材料。

本地化改造：
- 将 battle card 思路改造成“商家营销作战卡”。
- 输出从销售异议处理变为：爆款标题公式、内容策略、线索画像、私信话术。
- 后续可新增 `marketing_battle_card.html`，方便营销团队直接给商家汇报。

### AI Competitor Intelligence Agent Team

可借鉴点：
- 将外部数据抓取、分析、对比拆成独立 Agent。
- 支持 URL 或业务描述作为输入，降低用户使用门槛。
- 输出竞品对比表和策略建议，适合业务决策。

本地化改造：
- 当前版本暂不直接抓取小红书，避免反爬和合规风险。
- 先支持“人工导入评论 CSV / 商家信息 / 竞品信息”。
- 后续新增 `CompetitorAgent`：分析同城竞品标题、价格、卖点和评论痛点。

### AI Services Agency

可借鉴点：
- 用“虚拟团队”包装多 Agent，更容易被非技术用户理解。
- Streamlit 页面按角色分区展示结果。
- 每个 Agent 对应一个真实业务岗位。

本地化改造：
- 保留当前四角色命名：爆款分析员、文案生成师、线索挖掘员、外联专员。
- 前端展示从技术日志转为“营销团队工作台”。
- 后续增加每个 Agent 的执行摘要、耗时、输出质量评分。

## 我们项目的改造原则

1. **稳定优先**：核心演示仍使用本地 mock pipeline，不让外部 API 或框架依赖影响可运行性。
2. **Provider 解耦**：模型调用统一走 `providers/`，后续接小浣熊、OpenAI、Qwen、DeepSeek 不改 Agent 主逻辑。
3. **数据源解耦**：真实数据接入放到 `tools/`，包括 CSV、飞书表格、合规搜索 API、CRM。
4. **产物专业化**：输出不只停留在 JSON/CSV，逐步升级为营销简报、作战卡、可复制话术库。
5. **本地化表达**：面向小红书、本地生活、商家代运营、私域触达，而不是海外 SaaS 销售场景。

## 近期可落地改造

### V1.1：营销作战卡

新增 HTML/Markdown 简报，聚合当前四个 Agent 的结果：
- 商家基本信息
- 爆款标题公式
- 推荐发布时间和标签
- 3 篇文案摘要
- 高意向线索统计
- 触达话术样例

验收标准：
- pipeline 额外生成 `marketing_brief.md`。
- zip 包中包含该简报。
- Streamlit 增加“营销简报”Tab。

### V1.2：竞品分析 Agent

新增 `CompetitorAgent`，先用 mock/人工输入数据：
- 输入：竞品名称、价格、人均、主打卖点、评论痛点。
- 输出：竞品弱点、差异化卖点、内容切入角度。

验收标准：
- 不依赖爬虫也能运行。
- Copy Agent 可消费竞品分析，生成更有差异化的文案。

### V1.3：导入真实评论 CSV

新增数据源工具：
- 用户上传评论 CSV。
- Lead Agent 基于真实评论打分。
- 没有上传时回退 mock 数据。

验收标准：
- Streamlit 支持 CSV 上传。
- 上传数据至少包含 `username`、`comment`。
- 输出仍保持 `leads.csv` 标准结构。

### V1.4：多 Provider 实际接入

在保持 mock 可用的基础上补齐：
- `openai_provider.py`
- `xiaohuanxiong_provider.py`
- 可选 `qwen_provider.py` 或 `deepseek_provider.py`

验收标准：
- `.env` 切换 `MODEL_PROVIDER` 后无需改 Agent。
- Provider 失败有清晰错误提示。
- 不提交任何密钥。

## 参赛包装建议

对外讲法：

> 我们参考优秀多 Agent 应用模板的工程组织方式，但针对中国本地生活营销场景做了本地化改造：把海外 SaaS 的 battle card、竞品分析、虚拟 agency 模式，转换为小红书爆款分析、线索挖掘、商家文案和私信触达工作流。

演示重点：
- 不讲“用了几个 Agent”本身，而讲“营销团队一天的工作如何被拆成四个可复用岗位”。
- 展示最终 zip 包，让评委看到这是可交付产物，不只是聊天窗口。
- 强调 Provider 抽象：后续可接小浣熊办公版，适合国产模型生态。
