
async def _create_cat(client, name="Food", **extra):
    payload = {"name": name, **extra}
    r = await client.post("/api/v1/categories", json=payload)
    assert r.status_code in (200, 201), r.text
    body = r.json()
    return body, body.get("id") or body.get("_id")


async def test_list_empty(client):
    r = await client.get("/api/v1/categories")
    assert r.status_code == 200
    assert len(r.json()) == 0


async def test_create_and_get(client):
    body, cat_id = await _create_cat(client, name="Food")
    assert body.get("name") == "Food"
    assert cat_id is not None


async def test_create_duplicate_name_conflict(client):
    await _create_cat(client, name="Dup")
    r = await client.post("/api/v1/categories", json={"name": "Dup"})
    assert r.status_code == 409


async def test_create_invalid_payload(client):
    r = await client.post("/api/v1/categories", json={})
    assert r.status_code == 422


async def test_get_invalid_id(client):
    r = await client.get("/api/v1/categories/not-an-objectid")
    assert r.status_code == 405


async def test_update_and_delete(client):
    _, cat_id = await _create_cat(client, name="Temp")
    r = await client.put(f"/api/v1/categories/{cat_id}", json={"name": "Temp2"})
    assert r.status_code == 200
    r = await client.delete(f"/api/v1/categories/{cat_id}")
    assert r.status_code in (200, 204)
    r = await client.get("/api/v1/categories")
    assert "Temp2" not in [c["name"] for c in r.json()]