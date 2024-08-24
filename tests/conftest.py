
# Run: $ python -m pytest --disable-warnings

import httpx
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from api.models.agreements import Agreement, AgreementTeam, Company
from api.models.events import Event, Participation, Review, Path
from api.models.feedbacks import Feedback, FeedbackAnswer
from api.models.posts import Post, Tag, PostTag, Comment, CommentReaction
from api.models.teams import Team, Location
from api.models.users import Role, User, Profile, Motorcycle, Brand
from api.models.utils import seeders
from core.config import app
from core.database import get_db_session



@pytest.fixture(scope="session")
def anyio_backend():
    """Ensure that any test marked with 'anyio' uses 'asyncio' as backend."""

    return "asyncio"



@pytest.fixture(name="session", scope="session")
def session_fixture():
    """Return a session of a test database."""

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    seeders.insert_records(seeders.locations, Location, engine)
    seeders.insert_records(seeders.paths, Path, engine)
    seeders.insert_records(seeders.companies, Company, engine)
    seeders.insert_records(seeders.roles, Role, engine)
    seeders.insert_records(seeders.teams, Team, engine)
    seeders.insert_records(seeders.users, User, engine)
    seeders.insert_records(seeders.members, Profile, engine)
    seeders.insert_records(seeders.brands, Brand, engine)
    seeders.insert_records(seeders.motorcycles, Motorcycle, engine)
    seeders.insert_records(seeders.agreements, Agreement, engine)
    seeders.insert_records(seeders.agreement_teams, AgreementTeam, engine)
    seeders.insert_records(seeders.events, Event, engine)
    seeders.insert_records(seeders.participations, Participation, engine)
    seeders.insert_records(seeders.reviews, Review, engine)
    seeders.insert_records(seeders.tags, Tag, engine)
    seeders.insert_records(seeders.posts, Post, engine)
    seeders.insert_records(seeders.post_tags, PostTag, engine)
    seeders.insert_records(seeders.post_comments, Comment, engine)
    seeders.insert_records(seeders.comment_reactions, CommentReaction, engine)
    seeders.insert_records(seeders.feedbacks, Feedback, engine)
    seeders.insert_records(seeders.feedback_answers, FeedbackAnswer, engine)
    with Session(engine) as session:
        yield session



@pytest.fixture(name="client", scope="session")
async def client_fixture(session):
    """Return a async test client."""

    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client
        app.dependency_overrides.clear()
