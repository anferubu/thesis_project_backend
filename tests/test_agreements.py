import pytest
from sqlmodel import select



@pytest.mark.anyio
async def test_create_team(client, session):
    # Create team
    data = {
        "name": "Nuevo Equipo",
        "location_id": 567,
    }
    response = await client.post("/teams", json=data)
    print("-->", response.json())
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    # Validate the team in database
    from api.models.teams import Team
    query = select(Team).where(Team.name == data["name"])
    team = session.exec(query).first()
    assert team is not None
