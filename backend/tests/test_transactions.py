from datetime import datetime, timezone


async def _create_cat(client, name="Food", type_="expense"):
    r = await client.post("/api/v1/categories", json={"name": name})
    assert r.status_code in (200, 201), r.text
    b = r.json()
    return b.get("id") or b.get("_id")


async def _create_tx(client, cat_id, amount=100, type_="expense",
                     description="Lunch", date=None):
    payload = {
        "amount": amount,
        "type": type_,
        "category_id": cat_id,
        "description": description,
        "date": date or datetime.now(timezone.utc).isoformat(),
    }
    return await client.post("/api/v1/transactions", json=payload)


async def test_create_transaction(client):
    cat_id = await _create_cat(client)
    r = await _create_tx(client, cat_id)
    assert r.status_code in (200, 201), r.text


async def test_amount_must_be_positive(client):
    cat_id = await _create_cat(client)
    r = await _create_tx(client, cat_id, amount=-5)
    assert r.status_code == 422


async def test_invalid_category_id(client):
    r = await _create_tx(client, cat_id="000000000000000000000000")
    assert r.status_code in (400, 404)


async def test_list_and_filter_by_type(client):
    cat_exp = await _create_cat(client, name="Food")
    cat_inc = await _create_cat(client, name="Salary")
    await _create_tx(client, cat_exp, amount=50)
    await _create_tx(client, cat_inc, amount=500)

    r = await client.get("/api/v1/transactions", params={"type": "expense"})
    assert r.status_code == 200
    items = r.json() if isinstance(r.json(), list) else r.json().get("items", [])
    assert all(t["type"] == "expense" for t in items)


async def test_pagination(client):
    cat_id = await _create_cat(client)
    for i in range(5):
        await _create_tx(client, cat_id, description=f"tx{i}")

    r = await client.get("/api/v1/transactions", params={"limit": 2, "skip": 0})
    assert r.status_code == 200
    items = r.json() if isinstance(r.json(), list) else r.json().get("items", [])
    assert len(items) <= 2


async def test_search_by_description(client):
    cat_id = await _create_cat(client)
    await _create_tx(client, cat_id, description="Coffee with team")
    await _create_tx(client, cat_id, description="Taxi home")

    r = await client.get("/api/v1/transactions", params={"search": "Coffee"})
    assert r.status_code == 200
    items = r.json() if isinstance(r.json(), list) else r.json().get("items", [])
    assert any("Coffee" in t.get("description", "") for t in items)
