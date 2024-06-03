from sqlmodel import Session

from core.auth.models import User
from core.auth.schemas import UserCreate, UserUpdate
from core.auth.utils import get_password_hash



def create_user(session:Session, user_create:UserCreate) -> User:
    """
    Create a new user.

    Args:
    - session (Session): The database session to use for the operation.
    - user_create (UserCreate): The user data to create the new user.

    Returns:
    - User: The created user object.
    """

    new_user = User.model_validate(
        user_create,
        update={"password": get_password_hash(user_create.password)}
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user



def update_user(session:Session, db_user:User, user_in:UserUpdate) -> User:
    """
    Update an existing user.

    Args:
    - session (Session): The database session to use for the operation.
    - db_user (User): The current user object to update.
    - user_in (UserUpdate): The updated user data.

    Returns:
    - User: The updated user object.
    """

    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}

    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user