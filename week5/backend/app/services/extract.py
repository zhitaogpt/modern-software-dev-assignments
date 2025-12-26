import re

def extract_tags(text: str) -> list[str]:
    return re.findall(r"#(\w+)", text)

def extract_action_items(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        line = line.strip()
        # Match "- [ ] task" or "TODO: task" or "Task!"
        if line.startswith("- [ ]"):
            items.append(line[5:].strip())
        elif line.lower().startswith("todo:"):
            items.append(line[5:].strip())
        elif line.endswith("!"):
            items.append(line.strip("- !"))
    return items
