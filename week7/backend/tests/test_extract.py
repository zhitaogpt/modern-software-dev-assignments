from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - [ ] Complete documentation
    - FIXME: fix the bug
    - Task: call the client
    - Ship it!
    - [ ] Complete documentation
    Not actionable
    """.strip()
    items = extract_action_items(text)
    
    # Check new keywords (prefix removed by our regex captured group)
    assert "write tests" in items
    assert "review PR" in items
    assert "Complete documentation" in items
    assert "fix the bug" in items
    assert "call the client" in items
    assert "Ship it!" in items
    
    # Check deduplication
    assert items.count("Complete documentation") == 1
    
    # Check non-actionable
    assert "Not actionable" not in items


def test_extract_empty_or_no_match():
    assert extract_action_items("") == []
    assert extract_action_items("Just a regular sentence.") == []


