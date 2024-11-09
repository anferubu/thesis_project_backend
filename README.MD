# thesis_project_backend

Backend made in FastAPI for my degree project, which consists of an application to manage a motorcycle club.

# How to active the environment?

If environment doesn't exist:

```bash
python -m venv .venv
```

To active it:

```bash
source .venv/bin/activate
```

To deactivate it:

```bash
deactivate
```

# How to install dependencies?

With environment active:

```bash
pip install -r requirements.txt
```

# How to update the requirements file?

```bash
pip freeze > requirements.txt
```

# How to make migrations and create database?

1. Create migrations.

```bash
alembic revision --autogenerate -m <comment>
```

2. Upgrade migrations

```bash
alembic upgrade head
```

3. Create seeders on database

```bash
python -m api.models.utils.seeders
```

# How to run the development server?

Execute the command:

```bash
uvicorn main:app --reload
```
