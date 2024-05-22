from __future__ import annotations

import re
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

PYPROJECT_TOML_PATH = Path(__file__).resolve().parents[1] / "pyproject.toml"


def get_python_versions() -> list[str]:
    with PYPROJECT_TOML_PATH.open(mode="rb") as f:
        classifiers = tomllib.load(f)["project"]["classifiers"]

    return [
        version_match.group(1)
        for classifier in classifiers
        if (
            version_match := re.match(
                r"Programming Language :: Python :: (\d+\.\d+)",
                classifier,
            )
        )
    ]


def main() -> None:
    sys.stdout.write("\n".join(get_python_versions()))


if __name__ == "__main__":
    main()
