# Week 7 Write-up

## Submission Details
Name: AI Assistant
SUNet ID: N/A

## Pull Requests

### PR 1: Task 1 - Endpoints and Validations
- **Description**: Added input validation for note titles (1-200 chars), added `is_starred` field, and implemented `GET /notes/stats` and `PATCH /notes/{id}/star` endpoints.
- **Testing**: Added tests in `test_notes.py` covering validation errors (422) and star toggling.
- **Manual Review Findings**: 
    - Initially set title limit to 100 in schema while DB allowed 200, causing inconsistency.
    - Test case for title length was too short (101) after schema update to 200.
- **Graphite AI Review Comparison**: (To be filled by user)

### PR 2: Task 2 - Extraction Logic
- **Description**: Enhanced action item extraction using regex to support Markdown tasks (`- [ ]`), FIXME/TASK keywords, and case insensitivity. Added deduplication.
- **Testing**: Updated `test_extract.py` with complex Markdown and keyword examples.
- **Manual Review Findings**:
    - Discovered that premature `lstrip("- ")` in the service was breaking the regex for Markdown bullets.
    - Result format changed from returning the full line to just the content, which might be a breaking change for some UI consumers.
- **Graphite AI Review Comparison**: (To be filled by user)

### PR 3: Task 3 - New Model and Relationships
- **Description**: Introduced a `Tag` model and a many-to-many relationship with `Note`. Updated API to support tagging during creation and via a dedicated endpoint.
- **Testing**: Added `test_note_tags` to verify tag creation, association, and deduplication.
- **Manual Review Findings**:
    - Identified a potential mutable default argument issue in `schemas.py` (`tags: list[str] = []`), which was corrected to `default_factory=list`.
    - Potential N+1 query issue if tags are listed for many notes without `joinedload`.
- **Graphite AI Review Comparison**: (To be filled by user)

### PR 4: Task 4 - Pagination and Sorting Tests
- **Description**: Added a dedicated test suite for pagination and sorting logic to ensure stability across edge cases.
- **Testing**: New file `tests/test_pagination_sorting.py` with 20-note batch testing.
- **Manual Review Findings**:
    - Identified that timestamp precision might cause flakiness if multiple notes are created within the same millisecond, though currently mitigated by ID ordering in SQLite.
- **Graphite AI Review Comparison**: (To be filled by user)

## Reflection

### Manual Review Focus
In my manual reviews, I focused on:
- **Correctness/Consistency**: Matching database constraints with Pydantic schemas.
- **Edge Cases**: Empty titles, extremely long strings, and concurrent tag creation.
- **Best Practices**: Avoiding mutable defaults and ensuring idempotency (where applicable).

### Human vs. AI (Graphite) Comparison
(To be completed after Graphite Review)

### Trusting AI Reviews
(To be completed after Graphite Review)