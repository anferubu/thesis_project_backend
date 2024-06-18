"""
Defines a settings class to manage environment variables.

Environment variables must be defined in a .env file located in the root of
the project.

"""

from pydantic_settings import BaseSettings



class EnvSettings(BaseSettings):
    app_name: str
    app_version: str

    app_debug: bool

    secret_key: str

    database_url: str

    mail_server: str
    mail_port: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_from_name: str

    allowed_hosts: str
    allow_origins: str


env = EnvSettings(_env_file=".env")