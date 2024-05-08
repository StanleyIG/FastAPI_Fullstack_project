import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 201),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pesokot", 201),
    ("abcde", "pesokot", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("user@example.com", "user", 200),
    ("user2@person.com", "user2", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
