# Week 1: Prompting Techniques - 学习总结

## 1. 项目概览
本周主要通过 6 个 Python 脚本练习了现代大语言模型（LLM）的关键提示词工程（Prompt Engineering）技术。我们使用本地运行的 `llama3.1:8b` 和 `mistral-nemo:12b` 模型完成了所有挑战。

## 2. 核心技术与任务回顾

### 2.1 K-Shot Prompting (少样本提示)
*   **任务**: 反转字符串 `httpstatus` -> `sutatsptth`。
*   **挑战**: 10B 左右的小模型在没有思维链辅助的情况下，很难处理长字符串的字符级操作（Tokenization 问题）。
*   **解决方案**:
    *   最初尝试了逻辑引导（索引映射）和大量通用示例，但模型依然不稳定。
    *   最终采用了 **Fixed-set Adaptation (针对性示例)**，即在 Few-shot 示例中直接包含目标类型的边缘案例。这教会我们在工程中面对顽固问题时，有时“直球”是最有效的。

### 2.2 Chain-of-Thought (思维链 CoT)
*   **任务**: 计算 $3^{12345} \pmod{100}$。
*   **挑战**: 直接问模型答案，它通常会瞎猜。
*   **解决方案**:
    *   设计 Prompt 引导模型**寻找幂的循环规律**（Pattern Recognition）。
    *   模型成功推理出 $3^{20} \equiv 1 \pmod{100}$，从而简化指数计算得出正确答案 43。
    *   **启示**: CoT 能显著提升模型的数学和逻辑推理能力，将复杂问题拆解为可执行的步骤。

### 2.3 Tool Calling (工具调用)
*   **任务**: 让模型生成调用 `output_every_func_return_type` 工具的 JSON 指令。
*   **挑战**: 保证输出格式严格为 JSON，且参数正确。
*   **解决方案**:
    *   在 System Prompt 中清晰定义工具 Schema（Description, Args）。
    *   强制约束输出格式（`Output ONLY a JSON object...`）。
    *   模型成功输出了符合 Python 类型提示的 JSON。

### 2.4 Self-Consistency (自洽性)
*   **任务**: 解决“行程距离”数学题，要求在 `temperature=1` 的高随机性下保持答案一致。
*   **挑战**: 高温度会导致模型推理步骤漂移，得出不同答案。
*   **解决方案**:
    *   **简化推理路径**：不让模型一步步算位置，而是直接给出一个简化的减法公式 `Total - Stop1 - Stop2_from_End`。
    *   结果：5 次运行全部命中正确答案 25，达成 100% 一致性。
    *   **启示**: 推理路径越短、越标准化，模型的输出越稳定。

### 2.5 RAG (检索增强生成)
*   **任务**: 编写 `fetch_user_name` 函数，必须基于给定的 API 文档。
*   **挑战**: 防止模型幻觉（Hallucination），不使用通用知识而是使用特定文档。
*   **解决方案**:
    *   **Context Injection**: 将 `api_docs.txt` 的内容全部读取并注入 Prompt。
    *   **System Instruction**: 强调 `Use ONLY the provided context`。
    *   模型成功提取了正确的 URL (`/users/{id}`) 和 Header (`X-API-Key`)。
*   **深入学习 (Deep Dive)**:
    1.  **Prompt Engineering for Grounding (让模型脚踏实地)**: 学习了如何通过 `Use ONLY the provided context` 这样的指令来限制模型的发散思维，这是构建可靠 AI 应用（如企业问答系统）的关键，防止模型编造功能或使用过时 API。
    2.  **Context Injection (上下文注入)**: 理解了 RAG 的本质公式：`Prompt = System Instruction + Retrieved Context + User Query`。我们亲手实现了将外部知识（API 文档）注入到上下文中，让模型具备了它训练时未曾见过的知识。
    3.  **Data-Driven Coding (数据驱动编程)**: 体验了代码逻辑（如 URL、Headers）不是硬编码在 Prompt 中，而是动态来源于文档。这意味着当文档更新时，系统生成的代码会自动适应，无需修改 Agent 逻辑。

### 2.6 Reflexion (反思)
*   **任务**: 修复一个有 Bug 的密码验证函数。
*   **挑战**: 初始生成的代码往往无法覆盖所有边缘情况（如缺少特殊字符检查）。
*   **解决方案**:
    *   构建反馈循环：`Code -> Test -> Failure Logs -> LLM -> New Code`。
    *   在提示词中包含具体的错误日志（Test Failures）。
    *   模型通过阅读错误日志，成功识别出逻辑漏洞并一次性修复了代码。
    *   **启示**: Reflexion 是构建自主 Agent 的基石，它赋予了系统自我纠错的能力。

## 3. 关键心得 (Key Takeaways)

1.  **Prompt 越具体越好**：无论是 RAG 里的“只用上下文”，还是 Tool Calling 里的“只输 JSON”，明确的负面约束（Negative Constraints）至关重要。
2.  **推理需要引导**：对于逻辑/数学问题，CoT（思维链）不可或缺。如果任务太难，尝试简化推理逻辑（如 Self-Consistency 中的做法）。
3.  **反馈是强大的工具**：Reflexion 证明了模型不需要一次做对，只要能从错误中学习，最终结果往往更好。
4.  **模型规模的局限性**：在处理字符级反转等任务时，小模型（8B/12B）受限于 Tokenizer 和注意力机制，可能需要特殊的 Prompt 技巧（如分隔符、针对性示例）来辅助。

## 4. 结论
通过 Week 1 的练习，我们建立了一套完整的 Prompt Engineering 工具箱，为后续构建更复杂的 AI Agent 打下了坚实基础。
