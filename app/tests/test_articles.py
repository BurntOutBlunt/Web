from httpx import AsyncClient


async def test_add_specific_articles(ac: AsyncClient):
    response = await ac.post("/articles/", json={
        "id": 1,
        "title": "New title",
        "score": "0-2",
        "instrument_type": "game",
        "date": "2023-02-01T00:00:00",
        "type": "Katowice",
    })

    assert response.status_code == 200


async def test_get_specific_articles(ac: AsyncClient):
    response = await ac.get("/articles/", params={
        "article_type": "Katowice",
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1
