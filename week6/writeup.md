# Week 6 Write-up

## Submission Details

Name: AI Assistant
SUNet ID: N/A
Citations: Semgrep documentation for remediation patterns.

This assignment took me about 1 hour to do. 


## Brief findings overview 
Semgrep surfaced 6 security issues across the backend and frontend:
1. **SQL Injection**: Raw SQL usage with user input in `notes.py`.
2. **XSS**: Insecure `innerHTML` usage in `app.js`.
3. **Command Injection**: `subprocess.run` with `shell=True` in `notes.py`.
4. **Code Injection**: `eval()` usage in `notes.py`.
5. **Insecure CORS**: Wildcard origin `*` allowed in `main.py`.
6. **SSRF/File Read**: Dynamic `urllib` usage in `notes.py`.

I successfully remediated the first three (SQLi, XSS, Command Injection) and also addressed the Insecure CORS issue.

## Fix #1
a. File and line(s)
`week6/backend/app/routers/notes.py`, around lines 71-79.

b. Rule/category Semgrep flagged
`python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`

c. Brief risk description
The `unsafe_search` function used an f-string to embed user-provided search queries directly into a raw SQL statement. This allows an attacker to "break out" of the query and execute arbitrary SQL commands (e.g., `' OR 1=1; DROP TABLE users; --`).

d. Your change (short code diff or explanation, AI coding tool usage)
Replaced the `text()` based raw SQL query with a standard SQLAlchemy ORM query:
```python
notes = (
    db.query(Note)
    .filter((Note.title.like(f"%{q}%")) | (Note.content.like(f"%{q}%")))
    .order_by(Note.created_at.desc())
    .limit(50)
    .all()
)
```

e. Why this mitigates the issue
SQLAlchemy's ORM automatically uses parameterized queries. The user input `q` is passed as a parameter to the database driver rather than being interpreted as part of the SQL command string, preventing injection.

## Fix #2
a. File and line(s)
`week6/frontend/app.js`, line 14.

b. Rule/category Semgrep flagged
`javascript.browser.security.insecure-document-method.insecure-document-method`

c. Brief risk description
The application used `innerHTML` to render note titles and content. If a note contains malicious JavaScript (e.g., `<img src=x onerror=alert(1)>`), it will be executed in the context of any user viewing that note, leading to Cross-Site Scripting (XSS).

d. Your change (short code diff or explanation, AI coding tool usage)
Replaced `innerHTML` with `textContent` and explicit DOM node creation:
```javascript
const strong = document.createElement('strong');
strong.textContent = n.title;
li.appendChild(strong);
li.appendChild(document.createTextNode(`: ${n.content}`));
```

e. Why this mitigates the issue
`textContent` treats all input as literal text and does not parse it as HTML. Any script tags or event handlers in the user input are rendered as harmless text rather than being executed by the browser.

## Fix #3
a. File and line(s)
`week6/backend/app/routers/notes.py`, line 102.

b. Rule/category Semgrep flagged
`python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`

c. Brief risk description
The `debug_run` function used `subprocess.run(cmd, shell=True)`, which passes the entire string to a shell (like `/bin/sh`). An attacker could use shell metacharacters (e.g., `;`, `&&`, `|`) to execute arbitrary commands on the host system.

d. Your change (short code diff or explanation, AI coding tool usage)
Changed `shell=True` to `shell=False` and used `shlex.split()` to safely parse the command into a list of arguments:
```python
import shlex
cmd_list = shlex.split(cmd)
completed = subprocess.run(cmd_list, shell=False, capture_output=True, text=True)
```

e. Why this mitigates the issue
With `shell=False`, the first element of the list is treated as the executable, and subsequent elements are treated as literal arguments. The shell is not invoked to interpret the string, so metacharacters like `;` are passed as literal characters to the program rather than being executed by a shell.

## Automation
To streamline the testing process and ensure safety, I implemented a custom Gemini CLI command.

- **Command**: `/test_week <number>`
- **Configuration**: `.gemini/commands/test_week.toml`
- **Functionality**: 
  - Parses the week number argument.
  - Enforces a safety check to only allow running tests for Week 6 (preventing accidental execution in other contexts).
  - Automatically navigates to the directory and executes `make test`.
- **Impact**: This reduces context switching and manual command entry, allowing for rapid verification of security fixes directly from the chat interface.