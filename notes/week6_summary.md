# Week 6 Summary: Security & Automation

## Core Learning Objectives
1.  **Static Application Security Testing (SAST)**: Learned to use tools like Semgrep to identify vulnerabilities (SQLi, XSS, Command Injection).
2.  **Remediation**: Practiced fixing identified security flaws by using safer patterns (ORM vs Raw SQL, `textContent` vs `innerHTML`).
3.  **Agentic Automation**: Explored how to extend the coding assistant's capabilities with custom context-aware commands.

## Technical Implementation
- **Security Fixes**:
    - **SQL Injection**: Migrated to SQLAlchemy ORM methods.
    - **XSS**: Switched to `textContent` for safe DOM rendering.
    - **Command Injection**: Disabled `shell=True` and used `shlex.split()`.
- **Infrastructure**:
    - Created `.gemini/commands/test_week.toml` using TOML syntax.
    - Defined a prompt template with conditional logic to handle user arguments securely.

## Key Automations
- **`/test_week` Command**: A custom CLI tool that encapsulates the testing logic. It demonstrates how to "teach" the agent project-specific workflows, ensuring consistent test execution parameters.
