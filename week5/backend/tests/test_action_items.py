def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    envelope = r.json()
    item = envelope["data"]
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    envelope = r.json()
    done = envelope["data"]
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    envelope = r.json()
    paginated = envelope["data"]
    items = paginated["items"]
    # Depending on previous tests, there might be more, but at least this one
    assert any(i["id"] == item["id"] for i in items)

def test_action_items_filtering(client):
    # Create fresh items for this test
    client.post("/action-items/", json={"description": "Task Pending"})
    r = client.post("/action-items/", json={"description": "Task Completed"})
    item_comp = r.json()["data"]
    client.put(f"/action-items/{item_comp['id']}/complete")

    # Filter pending
    r = client.get("/action-items/", params={"completed": False})
    envelope = r.json()
    items = envelope["data"]["items"]
    # Verify we got results and all are pending
    assert len(items) > 0
    assert all(i["completed"] is False for i in items)
    
    # Filter completed
    r = client.get("/action-items/", params={"completed": True})
    envelope = r.json()
    items = envelope["data"]["items"]
    assert len(items) > 0
    assert all(i["completed"] is True for i in items)

def test_bulk_complete(client):
    r1 = client.post("/action-items/", json={"description": "Bulk 1"})
    r2 = client.post("/action-items/", json={"description": "Bulk 2"})
    ids = [r1.json()["data"]["id"], r2.json()["data"]["id"]]

    r = client.post("/action-items/bulk-complete", json={"item_ids": ids})
    assert r.status_code == 200
    res = r.json()
    assert res["ok"] is True
    assert res["data"]["count"] == 2
    
    # Verify completion
    r = client.get("/action-items/", params={"completed": True})
    items = r.json()["data"]["items"]
    completed_ids = [i["id"] for i in items]
    assert set(ids).issubset(set(completed_ids))
