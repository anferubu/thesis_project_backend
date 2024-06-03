# ¿Cómo crear una nueva tabla en la base de datos?

1. Crear una subclase de SQLModel que represente la tabla.

2. Importar la clase al final del archivo core/database/db.py.

3. Ejecutar el siguiente comando para crear el archivo de migración:
   $ alembic revision --autogenerate -m "<comment>"

4. Ejecutar el siguiente comando para ejecutar la migración y crear la tabla:
   $ alembic upgrade head