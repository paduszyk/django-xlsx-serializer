from __future__ import annotations

from itertools import chain

import nox

PYTHON_VERSIONS = [
    "3.9",
    "3.10",
    "3.11",
    "3.12",
]

DJANGO_VERSIONS = {
    "3.9": ["3.2", "4.0", "4.1", "4.2"],
    "3.10": ["3.2", "4.0", "4.1", "4.2", "5.0"],
    "3.11": ["4.1", "4.2", "5.0"],
    "3.12": ["4.2", "5.0"],
}

DATABASE_ENGINES = [
    "postgresql",
    "sqlite3",
]

RUFF_CHECK_OPTIONS = [
    "--output-format=github",
]

RUFF_FORMAT_OPTIONS = [
    "--diff",
]

MYPY_OPTIONS = [
    "--install-types",
    "--non-interactive",
]

PYTEST_OPTIONS = [
    "-ra",
    "-vv",
]


# Nox
# https://nox.thea.codes/


@nox.session(tags=["install"])
@nox.parametrize("python", PYTHON_VERSIONS)
def install(session: nox.Session) -> None:
    session.install(".")


@nox.session(tags=["lint"])
def ruff_lint(session: nox.Session) -> None:
    session.install("ruff")

    session.run("ruff", "check", *RUFF_CHECK_OPTIONS, ".")


@nox.session(tags=["lint"])
def ruff_format(session: nox.Session) -> None:
    session.install("ruff")

    session.run("ruff", "format", *RUFF_FORMAT_OPTIONS, ".")


@nox.session(tags=["lint"])
def mypy(session: nox.Session) -> None:
    session.install("-e", ".")
    session.install(
        "django-stubs[compatible-mypy] < 6",
        "psycopg2-binary < 3",
        "python-dotenv < 2",
        "types-openpyxl < 4",
    )

    session.run("mypy", *MYPY_OPTIONS, ".")


@nox.session(tags=["test"])
@nox.parametrize("database_engine", DATABASE_ENGINES)
@nox.parametrize(
    ("python", "django"),
    chain.from_iterable(
        [
            (python_version, django_version)
            for django_version in DJANGO_VERSIONS[python_version]
        ]
        for python_version in PYTHON_VERSIONS
    ),
)
def pytest(session: nox.Session, django: str, database_engine: str) -> None:
    session.install(f"django == {django}.*")
    session.install("-e", ".")
    session.install(
        "psycopg2-binary < 3",
        "pytest < 9",
        "pytest-cov",
        "pytest-custom-exit-code < 1",
        "pytest-django < 5",
        "python-dotenv < 2",
    )

    session.run(
        "pytest",
        *PYTEST_OPTIONS,
        env={
            "DATABASE_ENGINE": database_engine,
        },
    )
