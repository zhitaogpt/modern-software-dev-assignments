def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert data["is_starred"] is False
    assert "created_at" in data and "updated_at" in data

    # Test Validation: Empty title
    r = client.post("/notes/", json={"title": "", "content": "fail"})
    assert r.status_code == 422

    # Test Validation: Title too long
    r = client.post("/notes/", json={"title": "a" * 201, "content": "fail"})
    assert r.status_code == 422

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"

    # Test Starring
    r = client.patch(f"/notes/{note_id}/star")
    assert r.status_code == 200
    assert r.json()["is_starred"] is True

    r = client.patch(f"/notes/{note_id}/star")
    assert r.status_code == 200
    assert r.json()["is_starred"] is False

    # Test Stats
    r = client.get("/notes/stats")
    assert r.status_code == 200
    stats = r.json()
    assert "total_count" in stats
    assert "starred_count" in stats


def test_note_tags(client):
    # Test create with tags
    payload = {"title": "Tagged Note", "content": "Content", "tags": ["work", "urgent"]}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert len(data["tags"]) == 2
    assert sorted([t["name"] for t in data["tags"]]) == ["urgent", "work"]
    
    note_id = data["id"]
    
    # Test add tag to existing
    r = client.post(f"/notes/{note_id}/tags", params={"tag_name": "new_tag"})
    assert r.status_code == 200
    data = r.json()
    assert len(data["tags"]) == 3
    assert any(t["name"] == "new_tag" for t in data["tags"])
    
    # Test reuse tag (should not duplicate)
    r = client.post(f"/notes/{note_id}/tags", params={"tag_name": "work"})
    assert r.status_code == 200
    data = r.json()
    assert len(data["tags"]) == 3


