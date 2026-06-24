"""End-to-end API tests against an in-memory SQLite database."""
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

TEST_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(
        TEST_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestSession = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
    await engine.dispose()


async def _auth(client, email="a@b.com", password="password123"):
    r = await client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


async def test_register_login_me(client):
    headers = await _auth(client)

    # duplicate registration is rejected
    dup = await client.post("/auth/register", json={"email": "a@b.com", "password": "password123"})
    assert dup.status_code == 409

    # wrong password
    bad = await client.post("/auth/login", json={"email": "a@b.com", "password": "nope12345"})
    assert bad.status_code == 401

    # correct login
    ok = await client.post("/auth/login", json={"email": "a@b.com", "password": "password123"})
    assert ok.status_code == 200 and ok.json()["access_token"]

    me = await client.get("/auth/me", headers=headers)
    assert me.status_code == 200 and me.json()["email"] == "a@b.com"


async def test_lists_require_auth(client):
    r = await client.get("/lists")
    assert r.status_code == 401


async def test_list_crud_and_templates(client):
    headers = await _auth(client)

    payload = {
        "name": "Famille",
        "items": [
            {"text": "Paul", "orientation": "both"},
            {"text": "Camille", "orientation": "horizontal"},
        ],
        "gap": 2,
        "is_template": False,
    }
    created = await client.post("/lists", json=payload, headers=headers)
    assert created.status_code == 201, created.text
    lid = created.json()["id"]
    assert created.json()["items"][1]["orientation"] == "horizontal"

    # a template
    tmpl = await client.post(
        "/lists",
        json={"name": "Modèle prénoms", "items": [], "is_template": True},
        headers=headers,
    )
    assert tmpl.status_code == 201

    # filtering
    all_lists = await client.get("/lists", headers=headers)
    assert len(all_lists.json()) == 2
    only_templates = await client.get("/lists?template=true", headers=headers)
    assert len(only_templates.json()) == 1 and only_templates.json()[0]["is_template"]

    # update
    upd = await client.put(f"/lists/{lid}", json={"name": "Famille élargie", "gap": 3}, headers=headers)
    assert upd.status_code == 200 and upd.json()["name"] == "Famille élargie" and upd.json()["gap"] == 3

    # delete
    assert (await client.delete(f"/lists/{lid}", headers=headers)).status_code == 204
    assert (await client.get(f"/lists/{lid}", headers=headers)).status_code == 404


async def test_ownership_isolation(client):
    a = await _auth(client, "a@b.com")
    b = await _auth(client, "b@b.com")
    created = await client.post("/lists", json={"name": "A list", "items": []}, headers=a)
    lid = created.json()["id"]
    # user B cannot see or touch user A's list
    assert (await client.get(f"/lists/{lid}", headers=b)).status_code == 404
    assert (await client.delete(f"/lists/{lid}", headers=b)).status_code == 404


async def test_favorites(client):
    headers = await _auth(client)
    grid = {"rows": 3, "cols": 4, "crossings": 1, "cells": [{"row": 0, "col": 0, "ch": "P"}]}
    created = await client.post(
        "/favorites", json={"name": "Ma grille", "grid": grid}, headers=headers
    )
    assert created.status_code == 201, created.text
    fid = created.json()["id"]
    assert created.json()["grid"]["cols"] == 4

    listing = await client.get("/favorites", headers=headers)
    assert len(listing.json()) == 1

    assert (await client.delete(f"/favorites/{fid}", headers=headers)).status_code == 204
    assert len((await client.get("/favorites", headers=headers)).json()) == 0
