
from datetime import datetime, timezone


async def _cat(client, name):
    r = await client.post("/api/v1/categories", json={"name": name})
    assert r.status_code in (200, 201), r.text
    return r.json().get("id") or r.json().get("_id")


async def _tx(client, cat_id, amount, type_):
    await client.post("/api/v1/transactions", json={
        "amount": amount,
        "type": type_,
        "category_id": cat_id,
        "description": "t",
        "date": datetime.now(timezone.utc).isoformat(),
    })


async def test_stats_empty(client):
    r = await client.get("/api/v1/statistics/summary")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


async def test_stats_with_data(client):
    inc = await _cat(client, "Salary")
    exp = await _cat(client, "Food")
    await _tx(client, inc, 1000, "income")
    await _tx(client, exp, 300, "expense")
    r = await client.get("/api/v1/statistics/summary")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)