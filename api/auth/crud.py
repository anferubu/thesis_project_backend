"""
Defines the CRUD operations for User table.

For the User table, includes:
  - create_user()
  - get_user_by_id()
  - get_user_by_email()
  - get_users()
  - update_user()
  - change_password()
  - delete_user()

"""

from typing import List
from sqlmodel import Session, select, and_

from api.auth.models import User
from api.auth.schemas import UserCreate, UserUpdate
from api.auth.security.hashing import get_password_hash



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



def get_user_by_id(session:Session, user_id:int) -> User|None:
    """
    Retrieve a user by their ID.

    Args:
      - session (Session): The database session to use for the operation.
      - user_id (int): The ID of the user to retrieve.

    Returns:
      - User|None: The user object if found, otherwise None.
    """

    return session.get(User, user_id)



def get_user_by_email(session:Session, email:str) -> User|None:
    """
    Retrieve a user by their email.

    Args:
      - session (Session): The database session to use for the operation.
      - email (str): The email of the user to retrieve.

    Returns:
      - User|None: The user object if found, otherwise None.
    """

    query = select(User).where(
        and_(
            User.email == email,
            User.status != "deleted"
        )
    )
    return session.exec(query).first()



def get_users(session:Session, skip:int=0, limit:int=10) -> List[User]:
    """
    Retrieve a list of active users with pagination.

    Args:
      - session (Session): The database session to use for the operation.
      - skip (int): The number of records to skip.
      - limit (int): The maximum number of records to return.

    Returns:
      - List[User]: A list of user objects.
    """

    query = select(User).where(User.status == "active").offset(skip).limit(limit)
    return session.exec(query).all()



def update_user(session:Session, user_id:int, user_update:UserUpdate) -> User:
    """
    Update an existing user.

    Args:
      - session (Session): The database session to use for the operation.
      - user_id (int): The ID of the user to update.
      - user_in (UserUpdate): The updated user data.

    Returns:
      - User: The updated user object.
    """

    user = session.get(User, user_id)

    if user:
        user_data = user_update.model_dump(exclude_unset=True)
        extra_data = {}

        # If password is present in the updated data, hash it
        if "password" in user_data:
            password = user_data.pop("password")
            extra_data["password"] = get_password_hash(password)

        user.sqlmodel_update(user_data, update=extra_data)

        session.add(user)
        session.commit()
        session.refresh(user)

    return user



def change_password(session:Session, user_id:int, new_password:str) -> User:
    """
    Change a user's password.

    Args:
      - session (Session): The database session to use for the operation.
      - user_id (int): The ID of the user whose password should be changed.
      - new_password (str): The new password for the user.

    Returns:
      - User: The user object with the updated password.
    """

    user = session.get(User, user_id)

    hashed_password = get_password_hash(new_password)
    user.password = hashed_password

    session.add(user)
    session.commit()
    session.refresh(user)

    return user



def delete_user(session:Session, user_id:int) -> bool:
    """
    Mark a user as 'deleted' by setting their status attribute.

    Args:
      - session (Session): The database session to use for the operation.
      - user_id (int): The ID of the user to mark as 'deleted'.

    Returns:
      - bool: True if the user was marked as 'deleted', False otherwise.
    """

    user = session.get(User, user_id)

    if not user:
        return False

    user.status = "deleted"

    session.add(user)
    session.commit()

    return True
