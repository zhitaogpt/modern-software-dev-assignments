# Week 4: Autonomous Coding Agent IRL (Gemini CLI Edition)

## 目标
利用 Gemini CLI 的原生功能（`GEMINI.md` 和 Custom Commands）构建自动化开发环境，并完成 Week 4 的实战任务。

## 映射方案
- **Context**: `CLAUDE.md` -> `week4/.gemini/GEMINI.md`
- **Automation**: `.claude/commands/test.md` -> `week4/.gemini/commands/test.toml`

## 实施步骤

### Phase 1: Infrastructure (配置基础设施)
1.  **Context Injection**: 
    - 创建 `week4/.gemini/GEMINI.md`。
    - 内容包括：项目概览 (FastAPI + SQLite)、关键命令 (`make run/test/lint`)、代码规范 (Black/Ruff)。
2.  **Workflow Automation**:
    - 创建 `week4/.gemini/commands/test.toml`。
    - 定义 `/test` 命令：执行 `make test`，并让 AI 分析结果。

### Phase 2: Implementation (实战开发)
3.  **Task**: 完成 `week4/docs/TASKS.md` 中的 "2) Add search endpoint for notes"。
4.  **Workflow**:
    - 运行 `/test` 确认基准状态。
    - 编写代码实现功能。
    - 再次运行 `/test` 验证修复。

### Phase 3: Documentation (交付)
5.  更新 `week4/writeup.md`，详细记录 Gemini CLI 的配置过程和使用体验。
