from core.secrets import env



SECRET_KEY = env.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

TOKEN_URL = "/login/access-token"