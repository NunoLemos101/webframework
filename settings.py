
VIEW_FILES = [
    "framework.auth.views",
    "views",
]

MODEL_FILES = [
    "framework.auth.models",
    "models"
]

MIDDLEWARE_CLASSES = [
    "framework.security.middleware.XFrameOptionsMiddleware",
    "framework.auth.middleware.BearerAuthenticationMiddleware",
]

DB_FILE = "db.sqlite3"

LOGIN_ENDPOINT = "/api/auth/login"
REGISTER_ENDPOINT = "/api/auth/register"
ME_ENDPOINT = "/api/auth/me"

X_FRAME_OPTIONS = "DENY"
