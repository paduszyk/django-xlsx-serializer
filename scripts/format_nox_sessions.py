from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any, Callable

SESSION_NAME_FORMATS = {
    "install": "Install package (Python {python})",
    "ruff_lint": "Lint package (Ruff)",
    "ruff_format": "Format package (Ruff)",
    "mypy": "Type-check package (Mypy)",
    "pytest": "Test package (Python {python}, Django {django}, {database_engine})",
}


CALL_SPEC_VALUE_FORMATTERS = {
    "database_engine": lambda value: {
        "postgresql": "PostgreSQL",
        "sqlite3": "SQLite",
    }[value],
}


def format_nox_session(session: dict[str, Any]) -> dict[str, str]:
    def get_session_call_spec_value_formatter(name: str) -> Callable[[str], str]:
        return CALL_SPEC_VALUE_FORMATTERS.get(name, lambda value: value)

    name = session["name"]
    python = session.get("python") or ""
    call_specs = {
        name: get_session_call_spec_value_formatter(name)(value)
        for name, value in session["call_spec"].items()
    }

    return {
        "name": session["session"],
        "job": SESSION_NAME_FORMATS[name].format(python=python, **call_specs),
    }


def format_nox_sessions(tag: str) -> str:
    sessions = json.loads(
        subprocess.check_output(
            f"{sys.executable} -m nox --tag {tag} --list-sessions --json".split(),  # noqa: S603
        ),
    )

    return json.dumps(list(map(format_nox_session, sessions)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", type=str)

    args = parser.parse_args()

    sys.stdout.write(format_nox_sessions(args.tag))


if __name__ == "__main__":
    main()
