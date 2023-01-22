import os


class Config:
    PORT = int(os.environ.get('PORT', 8000))
    DEBUG = bool(int(os.environ.get('DEBUG', 0)))
    DEBUG_TOOLBAR = bool(int(os.environ.get('DEBUG_TOOLBAR', 0)))
    DB_URL = os.environ.get('DB_URL', 'postgresql+asyncpg://postgres:1111111@pg_db/db_name')
    REDIS_HOST = os.environ.get('REDIS_HOST', '')
    REDIS_PORT = os.environ.get('REDIS_PORT', 0)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
    REDIS_TIMEOUT = os.environ.get('REDIS_TIMEOUT', 0.1)


i_config = Config()
