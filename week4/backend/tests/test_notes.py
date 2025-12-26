def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

def test_search_case_insensitive(client):
    # Setup
    client.post("/notes/", json={"title": "Python", "content": "Programming language"})
    
    # Search lowercase
    r = client.get("/notes/search/", params={"q": "python"})
    assert r.status_code == 200
    data = r.json()
    # Should match "Python"
    assert any(n["title"] == "Python" for n in data), "Search should be case-insensitive"
