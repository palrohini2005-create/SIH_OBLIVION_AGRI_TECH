"""Settings, read from the environment or a .env file.

Every value has a working default, so the service runs with no configuration at
all. Override any of them with an environment variable of the same name
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Where SQLAlchemy keeps the database. Relative paths are resolved against
    # the python_backend folder, so running from anywhere finds the same file.
    database_url: str = f"sqlite:///{BASE_DIR / 'portal.db'}"

    # Origins allowed to call this API with cookies. Must be exact: a wildcard
    # is not permitted alongside credentials.
    cors_origins: list[str] = ["http://127.0.0.1:3000", "http://localhost:3000"]

    # The same cookie name the Node and Java backends use, so the front end
    # behaves identically whichever one it is talking to.
    session_cookie: str = "Crop Disease Detection Demo"
    session_max_age: int = 60 * 60 * 24 * 7
    session_secure: bool = False


    # Folder holding the seed JSON, loaded the first time the database is built.
    seed_dir: Path = BASE_DIR / "data"


settings = Settings()
