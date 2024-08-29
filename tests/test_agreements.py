import pytest
from sqlmodel import select

from api.models.agreements import Agreement, Company



# Agreement tests

@pytest.mark.anyio
async def test_list_agreements(client, session):
    response = await client.get("/agreements")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_retrieve_agreement(client, session):
    response = await client.get("/agreements/1")
    assert response.status_code == 200
    agreement = session.get(Agreement, 1)
    assert agreement.name == response.json()["name"]


@pytest.mark.anyio
async def test_create_agreement(client, session):
    data = {
        "name": "Valid agreement",
        "description": "This should work",
        "start_date": "2023-01-01",
        "end_date": "2025-12-31",
        "company_id": 2
    }
    response = await client.post("/agreements", json=data)
    assert response.status_code == 201
    query = select(Agreement).where(Agreement.name == data["name"])
    agreement = session.exec(query).first()
    assert agreement is not None


@pytest.mark.anyio
async def test_create_agreement_invalid_dates(client, session):
    data = {
        "name": "Invalid Agreement",
        "description": "This should fail due to invalid dates",
        "start_date": "2025-07-15",
        "end_date": "2024-02-10",
        "company_id": 2
    }
    response = await client.post("/agreements", json=data)
    assert response.status_code == 422  # Unprocessable Entity
    query = select(Agreement).where(Agreement.name == data["name"])
    agreement = session.exec(query).first()
    assert agreement is None


@pytest.mark.anyio
async def test_update_agreement(client, session):
    data = {"name": "This is a new name"}
    response = await client.put("/agreements/1", json=data)
    assert response.status_code == 200
    query = select(Agreement).where(Agreement.name == data["name"])
    agreement = session.exec(query).first()
    assert agreement is not None


@pytest.mark.anyio
async def test_soft_delete_agreement(client, session):
    response = await client.delete("/agreements/1")
    assert response.status_code == 204
    agreement = session.get(Agreement, 1)
    assert agreement is not None
    assert agreement.deleted is True


@pytest.mark.anyio
async def test_hard_delete_agreement(client, session):
    response = await client.delete("/agreements/2?hard=true")
    assert response.status_code == 204
    agreement = session.get(Agreement, 2)
    assert agreement is None



# Company tests

@pytest.mark.anyio
async def test_list_companies(client, session):
    response = await client.get("/companies")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_retrieve_company(client, session):
    response = await client.get("/companies/1")
    assert response.status_code == 200
    company = session.get(Company, 1)
    assert company.name == response.json()["name"]


@pytest.mark.anyio
async def test_create_company(client, session):
    data = {
        "name": "Company name",
        "contact_name": "Company CEO",
        "contact_telephone": "3108984343",
        "contact_address": "Cra 110 # 13-67, Bogotá",
        "location_id": 567
    }
    response = await client.post("/companies", json=data)
    assert response.status_code == 201
    query = select(Company).where(Company.name == data["name"])
    company = session.exec(query).first()
    assert company is not None


@pytest.mark.anyio
async def test_update_company(client, session):
    data = {"name": "This is a new name"}
    response = await client.put("/companies/1", json=data)
    assert response.status_code == 200
    query = select(Company).where(Company.name == data["name"])
    company = session.exec(query).first()
    assert company is not None


@pytest.mark.anyio
async def test_soft_delete_company(client, session):
    response = await client.delete("/companies/1")
    assert response.status_code == 204
    company = session.get(Company, 1)
    assert company is not None
    assert company.deleted is True


@pytest.mark.anyio
async def test_hard_delete_company(client, session):
    response = await client.delete("/companies/2?hard=true")
    assert response.status_code == 204
    company = session.get(Company, 2)
    assert company is None
