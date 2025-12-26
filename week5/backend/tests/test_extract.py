from backend.app.services.extract import extract_action_items, extract_tags


def test_extract_action_items():
    text = """
    This is a note
    - [ ] New style task
    TODO: write tests
    Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "New style task" in items
    assert "write tests" in items
    assert "Ship it" in items

def test_extract_tags():
    text = "This is a #great note with #multiple tags"
    tags = extract_tags(text)
    assert "great" in tags
    assert "multiple" in tags
