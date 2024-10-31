import pytest
import asyncio


@pytest.mark.asyncio
async def test_ping_server(client):
    response = await client.get("/api/health_check/ping_application")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ping_database(client):
    response = await client.get("/api/health_check/ping_database")
    assert response.status_code == 200
