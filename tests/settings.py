from __future__ import annotations

__all__ = [
    "DATABASES",
    "DEFAULT_AUTO_FIELD",
    "INSTALLED_APPS",
]

import os

from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS

# Detect CI environment.

CI_VARIABLES = [
    "GITHUB_ACTIONS",
]

CI_RUN = any(map(os.getenv, CI_VARIABLES))

if not CI_RUN:
    from dotenv import load_dotenv

    load_dotenv()


# Databases.

DATABASE_CONFIGS = {
    "dummy": {
        "ENGINE": "django.db.backends.dummy",
    },
    "postgresql": {
        "ENGINE": "django.db.backends.postgresql",
        # If Django is run on CI, use the `postgres` Docker image:
        # https://hub.docker.com/_/postgres
        **(
            {
                "NAME": "postgres",
                "HOST": "localhost",
                "PORT": "5432",
                "USER": "postgres",
                "PASSWORD": "postgres",
            }
            if CI_RUN
            # Otherwise, read the configuration from local environment variables.
            # The variables can be set in the `.env` file, see `.env.example`.
            else {
                "NAME": os.getenv("POSTGRES_NAME", "postgres"),
                "HOST": os.getenv("POSTGRES_HOST", "localhost"),
                "PORT": os.getenv("POSTGRES_PORT", "5432"),
                "USER": os.getenv("POSTGRES_USER", "postgres"),
                "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            }
        ),
    },
    "sqlite3": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:" if CI_RUN else "db.sqlite3",
    },
}

DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "dummy")

try:
    DATABASES = {
        DEFAULT_DB_ALIAS: DATABASE_CONFIGS[DATABASE_ENGINE],
    }
except KeyError as e:
    msg = (
        f"{DATABASE_ENGINE!r} isn't a valid value for the 'DATABASE_ENGINE' variable "
        f"(use one of the following: {', '.join(map(repr, DATABASE_CONFIGS))})"
    )
    raise ImproperlyConfigured(msg) from e


# Models.

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Apps.

INSTALLED_APPS = [
    "xlsx_serializer",
    "tests",
]
