"""
Defines the exceptions handler for the auth module.

It includes:
  - UserNotFoundException
  - NotAuthenticatedException
  - IncorrectCredentialsException
  - InactiveUserException
  - InvalidTokenException
  - UserAlreadyRegisteredException
  - OldPasswordException
  - NewPasswordException

"""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import EmailStr



class UserNotFoundException(HTTPException):

    def __init__(self, email:EmailStr):
        """
        Exception 404 raised when a user is not found in the database.

        Args:
          - email (str): The email of the user that was not found.
        """

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )



class NotAuthenticatedException(HTTPException):

    def __init__(self):
        """
        Exception 401 raised when the current user is unauthenticated.
        """

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )



class IncorrectCredentialsException(HTTPException):

    def __init__(self):
        """
        Exception 401 raised when the provided credentials are incorrect. This
        exception is used to indicate that the authentication attempt failed
        due to incorrect email or password.
        """

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials!",
        )



class InactiveUserException(HTTPException):

    def __init__(self, email:EmailStr):
        """
        Exception 403 raised when the user account is inactive. This exception
        is used to indicate that the authentication attempt failed because the
        user account is inactive.

        Args:
          - email (str): The email of the user that is inactive.
        """

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {email} is inactive!",
        )



class InvalidTokenException(HTTPException):

    def __init__(self):
        """
        Exception 401 raised when the provided token is invalid or expired.
        This exception is used to indicate that the token verification attempt
        failed due to an invalid or expired token.
        """

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token!",
        )



class UserAlreadyRegisteredException(HTTPException):

    def __init__(self, email:EmailStr):
        """
        Exception 409 raised when the user is already registered. This
        exception is used to indicate that the registration attempt failed
        because the user is already registered.

        Args:
          - email (str): The email of the user that is already registered.
        """

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {email} is already registered!",
        )



class OldPasswordException(HTTPException):

    def __init__(self):
        """
        Exception 400 raised when the provided old password is incorrect. This
        exception is used to indicate that the password change attempt failed
        because the old password is incorrect.
        """

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect!",
        )



class NewPasswordException(HTTPException):

    def __init__(self):
        """
        Exception 400 raised when the new password is the same as the old
        password. This exception is used to indicate that the password change
        attempt failed because the new password cannot be the same as the old
        password.
        """

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the old password.",
        )
