def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    envelope = r.json()
    assert envelope["ok"] is True
    data = envelope["data"]
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    envelope = r.json()
    assert envelope["ok"] is True
    paginated = envelope["data"]
    assert len(paginated["items"]) >= 1

    # Search (merged into list endpoint)
    r = client.get("/notes/", params={"q": "Hello"})
    assert r.status_code == 200
    envelope = r.json()
    paginated = envelope["data"]
    assert len(paginated["items"]) >= 1
    assert any("Hello" in n["content"] for n in paginated["items"])

def test_notes_pagination_and_sorting(client):
    # Add multiple notes
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
    
    # Pagination
    r = client.get("/notes/", params={"page_size": 2, "page": 1, "sort": "title_asc"})
    assert r.status_code == 200
    envelope = r.json()
    data = envelope["data"]
    
    assert data["page_size"] == 2
    assert len(data["items"]) == 2
    
    # Check sorting (title_asc)
    titles = [n["title"] for n in data["items"]]
    assert titles == sorted(titles)

def test_note_tags_integration(client):
    payload = {"title": "Tagged Note", "content": "This is #important and #urgent"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note = r.json()["data"]
    
    tags = note["tags"]
    tag_names = {t["name"] for t in tags}
    assert "important" in tag_names
    assert "urgent" in tag_names
    
    # Verify reuse of tags
    r2 = client.post("/notes/", json={"title": "Another Note", "content": "Also #important"})
    note2 = r2.json()["data"]
    tags2 = note2["tags"]
    assert "important" in {t["name"] for t in tags2}
    
    # Check if they share the same tag ID (optional, but good for verification)
    tag1_id = next(t["id"] for t in tags if t["name"] == "important")
    tag2_id = next(t["id"] for t in tags2 if t["name"] == "important")
    assert tag1_id == tag2_id

def test_update_and_delete_note(client):
    r = client.post("/notes/", json={"title": "To Update", "content": "Old Content"})
    note_id = r.json()["data"]["id"]
    
    # Update
    r = client.put(f"/notes/{note_id}", json={"content": "New Content #updated"})
    assert r.status_code == 200
    updated = r.json()["data"]
    assert updated["content"] == "New Content #updated"
    assert updated["tags"][0]["name"] == "updated"
    
    # Delete
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 200
    
    # Verify gone
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404

def test_not_found(client):
    r = client.get("/notes/99999")
    assert r.status_code == 404
    
    r = client.put("/notes/99999", json={"title": "Ghost"})
    assert r.status_code == 404
    
    r = client.delete("/notes/99999")
    assert r.status_code == 404
