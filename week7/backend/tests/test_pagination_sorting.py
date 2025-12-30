import pytest
from datetime import datetime, timedelta

def test_pagination_and_sorting(client):
    # 1. Setup: Create a batch of notes with distinct titles and timestamps
    # Note: Backend timestamps are set on creation, so we might need to rely on title sorting 
    # or ensure creation order. 
    # For robust timestamp testing, we'd mock datetime, but here we'll rely on insertion order 
    # and title logic.
    
    titles = [f"Note {i:02d}" for i in range(1, 21)] # "Note 01" to "Note 20"
    created_ids = []
    
    for t in titles:
        r = client.post("/notes/", json={"title": t, "content": f"Content for {t}"})
        assert r.status_code == 201
        created_ids.append(r.json()["id"])
        
    # 2. Test Pagination
    # Case: Limit 5, Skip 0 -> Should get Note 20 to Note 16 (default sort is -created_at)
    r = client.get("/notes/", params={"limit": 5, "skip": 0})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5
    # Default sort is -created_at (newest first). Since we inserted 01 -> 20, 
    # 20 is newest.
    assert data[0]["title"] == "Note 20"
    assert data[4]["title"] == "Note 16"
    
    # Case: Limit 5, Skip 5 -> Should get Note 15 to Note 11
    r = client.get("/notes/", params={"limit": 5, "skip": 5})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5
    assert data[0]["title"] == "Note 15"
    assert data[4]["title"] == "Note 11"
    
    # 3. Test Sorting
    # Case: Sort by Title Ascending (Note 01, Note 02 ...)
    r = client.get("/notes/", params={"sort": "title", "limit": 20})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 20
    assert data[0]["title"] == "Note 01"
    assert data[-1]["title"] == "Note 20"
    
    # Case: Sort by Title Descending (Note 20, Note 19 ...)
    r = client.get("/notes/", params={"sort": "-title", "limit": 20})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 20
    assert data[0]["title"] == "Note 20"
    assert data[-1]["title"] == "Note 01"
    
    # Case: Sort by Created At Ascending (Oldest first -> Note 01)
    r = client.get("/notes/", params={"sort": "created_at", "limit": 5})
    assert r.status_code == 200
    data = r.json()
    assert data[0]["title"] == "Note 01"
    
    # 4. Test Edge Cases
    # Case: Skip beyond total
    r = client.get("/notes/", params={"skip": 100, "limit": 5})
    assert r.status_code == 200
    assert len(r.json()) == 0

