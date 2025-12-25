# Week 3 Summary: Building Advanced MCP Servers

## 1. 核心成就
本周成功从零构建了一个模块化、多功能的 **MCP (Model Context Protocol) Server**，实现了 AI 与外部世界的高级交互。

### 主要功能模块
*   **Hacker News (HN)**:
    *   实现了基于 Algolia API 的新闻抓取。
    *   增加了 `get_story_details` 工具，抓取高赞评论以辅助深度分析。
    *   结合 Gemini 原生 `web_fetch` 工具，实现了“列表 -> 筛选 -> 深度阅读”的高级总结工作流。
*   **Kalshi (预测市场)**:
    *   解决了公共 API 不支持搜索的痛点，采用了 **"Fetch All + Client-side BM25 Search"** 的策略。
    *   实现了基于内存 (In-memory) 的缓存机制，大幅提升了搜索响应速度。
    *   通过抓取预测市场数据（赔率），为 AI 提供了“舆论 vs 市场信心”的全新分析维度。

## 2. 关键技术点

### MCP 架构设计
*   **Modular Monolith (模块化单体)**: 采用 `week3/server/main.py` 作为入口，`tools/` 下分模块管理业务逻辑。这种架构既保持了部署的简单性，又具备良好的代码组织。
*   **Prompt Engineering in Code**: 在 MCP Server 端定义 Prompt（如 `summarize_hn_trends`），将复杂的 CoT (Chain of Thought) 逻辑固化为可复用的资产。

### 搜索与数据检索优化
*   **Rank-BM25**: 引入了轻量级文本检索算法 BM25，在无需外部向量数据库的情况下，实现了比简单正则匹配强大得多的本地搜索能力。
*   **Caching Strategy**: 针对低频更新的数据（如市场列表），使用简单的 `time.time()` 时间戳对比实现 TTL 缓存，显著减少了 API 调用开销。

### 调试与运维
*   **Gemini CLI Configuration**: 深入理解了 `~/.gemini/settings.json` 的配置结构，以及如何通过 `mcpServers` 字段挂载本地 Python 服务。
*   **热加载 (Hot Reloading)**: 掌握了在修改 MCP Server 代码后，通过重启 CLI 来生效变更的开发流程。

## 3. 经验教训 (Lessons Learned)
*   **API 的局限性是常态**: 不要轻信 API 文档的搜索能力（如 Kalshi）。当服务端能力不足时，客户端（Server 端代码）需要承担更多的数据处理责任（如全量拉取 + 本地过滤）。
*   **多模态工具链**: MCP 工具不应孤立存在。最佳实践是 MCP 工具提供“线索”（如 URL, Ticker），然后结合 LLM 原生的通用工具（如 `web_fetch`, `google_search`）进行深度加工。
*   **用户体验**: 工具返回的 JSON 数据虽然对 AI 友好，但对人类用户可能过于冗长。在设计 Prompt 时，应引导 AI 输出自然语言摘要，而非直接展示原始数据。

## 4. 未来展望
*   **向量化**: 引入 Embedding API 替代 BM25，实现真正的语义搜索（搜 "Crypto" 出 "Bitcoin"）。
*   **鉴权管理**: 为 Notion 等需要 Auth 的服务实现更安全的 Token 管理机制。
