# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Gemini Agent** 
SUNet ID: **gemini-bot** 
Citations: **None**

This assignment took me about **1** hours to do. 


## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Modeled after the `CLAUDE.md` best practice for context injection, adapted for Gemini CLI via `.gemini/GEMINI.md`. This ensures the agent has persistent knowledge of the project structure and conventions.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Provide the agent with "implicit knowledge" about the project (e.g., "always use black for formatting").
> **Inputs**: The file `.gemini/GEMINI.md` located in the project root.
> **Content**: Defined paths for Backend/Frontend/Data, specified `make` commands for running/testing, and enforced PEP 8/Async standards.
> **Output**: The agent automatically adheres to these standards in every response without needing repetitive prompting.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Run**: Automatically loaded by the Gemini CLI when opening the project.
> **Verify**: Use `/memory show` (if available) or simply ask "What is the command to run tests?" to verify context awareness.
> **Safety**: Read-only configuration. Safe to edit or remove.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before**: I had to tell the agent "This is a FastAPI app, please run tests with pytest" every time.
> **After**: The agent knows the stack and commands immediately.

e. How you used the automation to enhance the starter application
> This automation served as the foundation. When I asked to "implement search", the agent already knew where `routers` were and that it should add tests to `backend/tests/`, significantly speeding up the planning phase.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the "Custom slash commands" requirement. I implemented `/test` to automate the Test-Driven Development (TDD) loop.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Run tests and analyze failures in one step.
> **Inputs**: `/test` command.
> **Steps**: 1. Execute `cd week4 && make test`. 2. Capture stdout/stderr. 3. Feed output to LLM with a prompt to analyze failures or summarize success.
> **Output**: A concise report on test health.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Run**: Type `/test` in the CLI.
> **Output**: "Tests Passed" summary or detailed "Root Cause Analysis" for failures.
> **Safety**: Runs standard test command. Safe.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before**: Manually run `make test` in terminal, paste output to LLM, ask "why did this fail?".
> **After**: Type `/test`. The agent handles execution and diagnosis instantly.

e. How you used the automation to enhance the starter application
> I used `/test` to verify the baseline state. Then, after modifying `backend/tests/test_notes.py` to add the search test case, I used `/test` to confirm the failure (Red). After implementing the backend and frontend logic, I used `/test` again to verify the fix (Green).


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> The `/learn` command. Designed to autonomously parse a new week's material and generate a learning plan.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Quickly understand a new directory's scope.
> **Inputs**: `/learn [directory_name]`.
> **Steps**: List files recursively -> Read `assignment.md` -> Analyze objectives -> Propose Plan.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Run**: `/learn week4`.
> **Output**: A structured learning plan with Phases (Understanding, Implementation, Verification).

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before**: Manually `ls`, `cat assignment.md`, then summarize.
> **After**: One command to get a briefing.

e. How you used the automation to enhance the starter application
> Used at the very beginning to analyze the `week4` directory and formulate the implementation strategy for the search feature.