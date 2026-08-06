from __future__ import annotations

from itertools import chain

import nox
import nox_uv

PYTHON_VERSIONS = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

DJANGO_VERSIONS = {
    "3.10": ["3.2", "4.0", "4.1", "4.2", "5.0", "5.1", "5.2"],
    "3.11": ["4.1", "4.2", "5.0", "5.1", "5.2"],
    "3.12": ["4.2", "5.0", "5.1", "5.2", "6.0", "6.1"],
    "3.13": ["5.1", "5.2", "6.0", "6.1"],
    "3.14": ["5.2", "6.0", "6.1"],
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

nox.options.default_venv_backend = "uv"


@nox_uv.session(tags=["install"])
@nox.parametrize("python", PYTHON_VERSIONS)
def install(session: nox.Session) -> None:
    pass


@nox_uv.session(tags=["lint"], uv_only_groups=["ruff"])
def ruff_lint(session: nox.Session) -> None:
    session.run("ruff", "check", *RUFF_CHECK_OPTIONS, ".")


@nox_uv.session(tags=["lint"], uv_only_groups=["ruff"])
def ruff_format(session: nox.Session) -> None:
    session.run("ruff", "format", *RUFF_FORMAT_OPTIONS, ".")


@nox_uv.session(tags=["lint"], uv_groups=["mypy"])
def mypy(session: nox.Session) -> None:
    session.run("mypy", *MYPY_OPTIONS, ".")


@nox_uv.session(tags=["test"], uv_groups=["pytest"])
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
    session.run(
        "pytest",
        *PYTEST_OPTIONS,
        env={
            "DATABASE_ENGINE": database_engine,
        },
    )
