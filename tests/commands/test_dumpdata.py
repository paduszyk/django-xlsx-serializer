from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import openpyxl
import pytest

from django.core.management import call_command

from xlsx_serializer.core import Serializer

from tests.models import DummyModel

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.django_db
def test_dumpdata_command_invokes_serializer(fixture_path: Path) -> None:
    # Arrange.
    DummyModel._default_manager.create()

    # Act.
    with mock.patch.multiple(
        Serializer,
        serialize=mock.DEFAULT,
        getvalue=mock.DEFAULT,
    ) as serializer_mock:
        call_command("dumpdata", format="xlsx", output=fixture_path)

    # Assert.
    serializer_mock["serialize"].assert_called()


@pytest.mark.django_db
def test_dumpdata_command_warns_if_output_is_not_provided() -> None:
    # Arrange.
    DummyModel._default_manager.create()

    # Act & assert.
    with pytest.warns(
        RuntimeWarning,
        match=r"printing workbooks to the standard output isn't supported",
    ):
        call_command("dumpdata", format="xlsx")


@pytest.mark.django_db
def test_dumpdata_command_warns_if_there_is_nothing_to_serialize(
    fixture_path: Path,
) -> None:
    # Arrange.
    call_command("flush", interactive=False)

    # Act & assert.
    with pytest.warns(
        RuntimeWarning,
        match=r"the output workbook is empty, so it won't be saved",
    ):
        call_command("dumpdata", format="xlsx", output=fixture_path)


@pytest.mark.django_db
def test_dumpdata_command_saves_workbook_if_output_is_provided(
    fixture_path: Path,
) -> None:
    # Arrange.
    DummyModel._default_manager.create()

    # Act.
    with mock.patch.object(openpyxl.Workbook, "save") as workbook_save_mock:
        call_command("dumpdata", format="xlsx", output=str(fixture_path))

    # Assert.
    workbook_save_mock.assert_called_with(str(fixture_path))


@pytest.mark.django_db
def test_dumpdata_command_does_not_save_workbook_if_output_is_not_provided() -> None:
    # Arrange.
    DummyModel._default_manager.create()

    # Act.
    with mock.patch.object(openpyxl.Workbook, "save") as workbook_save_mock:
        call_command("dumpdata", format="xlsx")

    # Assert.
    workbook_save_mock.assert_not_called()
