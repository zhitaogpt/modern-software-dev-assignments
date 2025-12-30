# Week 5 Plan: The Gemini-Native Agentic Workflow

本周的核心目标是在不依赖 Warp 图形界面的前提下，通过 **Gemini CLI** 和 **自定义脚本** 来实践 "Agentic Development"（代理式开发）和 "Multi-Agent"（多代理协作）理念。

## 核心目标
1.  **构建基础设施即代码 (Infrastructure as Code) 的自动化**：用可复用的脚本和 CLI 命令替代 GUI 配置（如 Warp Drive）。
2.  **模拟多代理 (Multi-Agent) 协作开发**：通过角色切换（Role-Playing）和工具委派（Delegation），在一个 CLI 会话中并行推进两个独立的特性开发，并解决集成问题。

## 任务范围
我们选择了 `TASKS.md` 中的两个中等难度任务，因为它们涉及全栈修改且相对独立，适合并行开发：
*   **任务 2：笔记搜索 (Notes Search)**：后端 API 支持搜索/分页，前端添加搜索 UI。
*   **任务 4：待办事项过滤 (Action Items Filters)**：后端 API 支持状态过滤/批量完成，前端添加过滤 UI。

---

## 分阶段执行计划

### 阶段 1：理解与基建 (Infrastructure & Automation)
目标：建立自动化工具，为开发铺路，替代 "Warp Drive"。

1.  **探索与环境确认**：
    *   阅读现有代码 (`backend`, `frontend`)。
    *   确保项目可运行 (`make run`) 和通过测试 (`make test`)。
2.  **构建自动化 A (Docs Sync)**：
    *   编写 `week5/scripts/sync_docs.py`：自动从 FastAPI 代码生成 Markdown 格式的 API 文档。
    *   配置 `.gemini/commands/sync-docs.toml`：注册为 `/sync-docs` 命令。
3.  **构建自动化 B (Smart Test Runner)**：
    *   编写 `week5/scripts/test_runner.py`：一个简单的测试运行器，可以接受参数来只运行相关的测试（例如只测 notes 或 action_items）。
    *   配置 `.gemini/commands/test.toml`：注册为 `/test` 命令。

### 阶段 2：多代理模拟开发 (Multi-Agent Simulation)
目标：通过角色扮演完成业务逻辑开发，模拟 Warp 的 "Tab 隔离" 开发模式。

1.  **Agent 1：搜索专家 (Search Specialist)**
    *   **角色定义**：专注于 `backend/app/routers/notes.py` 和前端搜索栏。
    *   **执行**：
        *   修改后端：实现 `GET /notes/search`。
        *   修改前端：添加 `<input id="search">` 并对接 API。
        *   单元测试：编写 `backend/tests/test_notes.py` 中的搜索测试。
2.  **Agent 2：效率专家 (Action Items Specialist)**
    *   **角色定义**：专注于 `backend/app/routers/action_items.py` 和前端过滤器。
    *   **执行**：
        *   修改后端：实现 `GET /action-items?completed=...` 和 `POST /bulk-complete`。
        *   修改前端：添加 Filter Buttons 和 Bulk Complete 按钮。
        *   单元测试：编写 `backend/tests/test_action_items.py` 中的过滤测试。

### 阶段 3：集成与交付 (Integration & Delivery)
目标：合并“两个 Agent”的工作成果，确保系统整体稳定。

1.  **集成测试**：运行完整的测试套件，检查是否有功能冲突。
2.  **文档同步**：运行 `/sync-docs`，自动更新 API 文档以包含新接口。
3.  **撰写 Writeup**：在 `week5/writeup.md` 中详细记录：
    *   我们是如何用 CLI 命令替代 Warp Drive 的。
    *   在单线程 CLI 中模拟多 Agent 协作的体验和思考。
