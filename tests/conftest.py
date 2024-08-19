from __future__ import annotations

import shutil
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Callable
from unittest import mock

import pytest

from django.conf import settings
from django.core.files import File
from django.core.files.images import ImageFile
from django.test.utils import override_settings

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(autouse=True)
def _media_setup_and_cleanup() -> Generator[None, None, None]:
    with override_settings(
        MEDIA_ROOT=Path(__file__).resolve().parent / "media",
    ):
        yield

        with suppress(FileNotFoundError):
            shutil.rmtree(settings.MEDIA_ROOT)


@pytest.fixture
def mock_file() -> Callable[[str], mock.Mock]:
    def _mock_file(filename: str) -> mock.Mock:
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = filename

        return file_mock

    return _mock_file


@pytest.fixture
def mock_image() -> Callable[[str], mock.Mock]:
    def _mock_image(filename: str) -> mock.Mock:
        image_file_mock = mock.MagicMock(spec=ImageFile)
        image_file_mock.name = filename

        return image_file_mock

    return _mock_image


@pytest.fixture
def fixture_path(tmp_path: Path) -> Path:
    return tmp_path / "fixture.xlsx"
