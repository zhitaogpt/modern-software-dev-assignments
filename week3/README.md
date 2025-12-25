# Week 3: Modular MCP Server (Hacker News & Kalshi)

## 1. 项目概述
这是一个高可扩展的 MCP Server，旨在封装多个外部 API（如 Hacker News 和 Kalshi），为 AI 提供丰富的数据上下文。通过该 Server，AI 可以实时获取技术新闻、深度评论以及预测市场的概率数据，从而进行多维度的趋势分析。

## 2. 架构设计
本项目采用 **模块化单体 (Modular Monolith)** 架构，方便未来扩展更多工具：

```text
week3/
├── pyproject.toml         # 依赖配置 (mcp, httpx, rank-bm25)
├── README.md              # 本文档
└── server/                # 源码目录
    ├── __init__.py
    ├── main.py            # 【入口】负责初始化 Server 和注册工具
    └── tools/             # 【业务逻辑】独立的功能模块
        ├── __init__.py
        ├── hn.py          # Hacker News 模块 (Algolia API)
        └── kalshi.py      # Kalshi 预测市场模块 (BM25 搜索 + 缓存)
```

## 3. 功能模块

### Hacker News 模块 (`hn.py`)
*   **`hn_get_hot_stories`**: 获取过去 N 小时内的高分文章。
*   **`hn_get_story_details`**: 获取特定文章的详细内容及**前 10 条高质量评论**，用于挖掘社区讨论的上下文。

### Kalshi 预测市场模块 (`kalshi.py`)
*   **`kalshi_search`**: 搜索预测市场。采用 **BM25 算法** 实现更智能的文本搜索（相比简单的关键词匹配）。
*   **`kalshi_details`**: 获取特定 Ticker 的详细赔率和规则。
*   **特性**：
    *   **内存缓存**：实现了 5 分钟 TTL 缓存，大幅减少 API 调用并提升响应速度。
    *   **全量索引**：一次性拉取 1000 条活跃市场数据，解决公共 API 不支持服务端搜索的局限。

## 4. 运行与配置

### 安装依赖
```bash
pip install mcp httpx rank-bm25
```

### 运行 Server
```bash
python -m week3.server.main
```

### 在 Gemini CLI / Claude Desktop 中配置
在 `~/.gemini/settings.json` 或 Claude 配置文件中添加：
```json
"mcpServers": {
  "week3-toolkit": {
    "command": "python3",
    "args": ["-m", "week3.server.main"],
    "env": {
      "PYTHONPATH": "/Users/guanxuan.zzt/repos/cs146s"
    }
  }
}
```

## 5. 高级用法 (Prompt)
Server 内置了 `summarize_hn_trends` 提示词，引导 AI 结合 `web_fetch` 工具进行深度新闻简报。建议通过以下方式调用：
> "请按照 summarize_hn_trends 的逻辑，为我总结过去 24 小时的技术动态。"
