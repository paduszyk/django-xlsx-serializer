from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest

from django.core.serializers import serialize
from django.core.serializers.base import SerializationError

from tests.models import (
    DummyModel,
    LabelLongerThan31CharactersModel,
    LabelLongerThan31CharactersModelA,
    LabelLongerThan31CharactersModelB,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.django_db()
def test_serializer_saves_workbook_if_stream_is_valid(fixture_path: Path) -> None:
    # Arrange.
    obj = DummyModel._default_manager.create()

    # Act.
    serialize("xlsx", [obj], stream=fixture_path)

    # Assert.
    assert fixture_path.exists()


def test_serializer_raises_error_if_stream_is_invalid() -> None:
    # Act & assert.
    with pytest.raises(
        SerializationError,
        match=r"the stream must be a file path 'str' or 'pathlib.Path' object",
    ):
        serialize("xlsx", [], stream=mock.ANY)


@pytest.mark.django_db()
def test_serializer_applies_shortened_sheet_name_if_model_label_is_too_long() -> None:
    # Arrange.
    obj = LabelLongerThan31CharactersModel._default_manager.create()

    # Act.
    wb = serialize("xlsx", [obj])

    # Assert.
    assert "LabelLongerThan31CharactersMode" in wb


@pytest.mark.django_db()
def test_serializer_emits_runtime_warning_if_model_label_is_too_long() -> None:
    # Arrange.
    obj = LabelLongerThan31CharactersModel._default_manager.create()

    # Act & assert.
    with pytest.warns(
        RuntimeWarning,
        match=(
            r"'tests.LabelLongerThan31CharactersModel' objects are serialized into "
            r"'LabelLongerThan31CharactersMode' sheet \(fully qualified label is too "
            r"long, 38 > 31\)"
        ),
    ):
        wb = serialize("xlsx", [obj])

    # Assert.
    assert "LabelLongerThan31CharactersMode" in wb


@pytest.mark.django_db()
def test_serializer_raises_error_if_conflicting_default_sheet_names_are_found() -> None:
    # Arrange.
    obj_a = LabelLongerThan31CharactersModelA._default_manager.create()
    obj_b = LabelLongerThan31CharactersModelB._default_manager.create()

    # Act & assert.
    with pytest.raises(
        SerializationError,
        match=(
            r"the truncated sheet name 'LabelLongerThan31CharactersMode' for "
            r"serializing the 'tests.LabelLongerThan31CharactersModelB' isn't unique; "
            r"use the 'model_sheet_names' option to manually resolve too long or "
            r"conflicting names"
        ),
    ):
        serialize("xlsx", [obj_a, obj_b])


@pytest.mark.django_db()
def test_serializer_applies_sheet_name_from_model_sheet_names_option() -> None:
    # Arrange.
    obj = DummyModel._default_manager.create()

    # Act.
    wb = serialize(
        "xlsx",
        [obj],
        model_sheet_names={
            "tests.DummyModel": "DummyModel",
        },
    )

    # Assert
    assert wb.sheetnames == ["DummyModel"]


def test_serializer_raises_error_if_model_identifier_from_model_sheet_names_option_is_not_valid() -> None:  # fmt: skip
    # Act & assert.
    with (
        mock.patch(
            "xlsx_serializer.core.apps.get_models",
            return_value=[
                mock.Mock(
                    _meta=mock.Mock(app_label="app", model_name="model"),
                ),
            ],
        ),
        pytest.raises(
            SerializationError,
            match=(
                r"invalid 'model_sheet_names' option: "
                r"model 'app.doesnotexist' isn't installed"
            ),
        ),
    ):
        serialize("xlsx", [], model_sheet_names={"app.doesnotexist": "DoesNotExist"})


def test_serializer_raises_error_if_model_identifier_from_model_sheet_names_option_is_ambiguous() -> None:  # fmt: skip
    # Act & assert.
    with (
        mock.patch(
            "xlsx_serializer.core.apps.get_models",
            return_value=[
                mock.Mock(_meta=mock.Mock(app_label="app_1", model_name="model")),
                mock.Mock(_meta=mock.Mock(app_label="app_2", model_name="model")),
            ],
        ),
        pytest.raises(
            SerializationError,
            match=(
                r"invalid 'model_sheet_names' option: "
                r"model 'model' found in multiple apps \('app_1', 'app_2'\); "
                r"use a fully qualified label to properly refer to the requested model"
            ),
        ),
    ):
        serialize("xlsx", [], model_sheet_names={"model": mock.ANY})


def test_serializer_raises_error_if_sheet_name_from_model_sheet_names_option_is_too_long() -> None:  # fmt: skip
    # Act & assert.
    with pytest.raises(
        SerializationError,
        match=(
            r"'CustomSheetNameLongerThan31Characters' is not a valid Excel sheet name "
            r"\(it is too long, 37 > 31\)"
        ),
    ):
        serialize(
            "xlsx",
            [],
            model_sheet_names={
                "tests.DummyModel": "CustomSheetNameLongerThan31Characters",
            },
        )


def test_serializer_raises_error_if_sheet_name_from_model_sheet_names_option_is_not_unique() -> None:  # fmt: skip
    # Act & assert.
    with pytest.raises(
        SerializationError,
        match=r"'DummyModel' is not a valid Excel sheet name \(it is not unique\)",
    ):
        serialize(
            "xlsx",
            [],
            model_sheet_names={
                "tests.DummyModelA": "DummyModel",
                "tests.DummyModelB": "DummyModel",
            },
        )


@pytest.mark.parametrize(
    "invalid_character",
    [
        "\\",
        "/",
        "?",
        "*",
        "[",
        "]",
    ],
)
def test_serializer_raises_error_if_sheet_name_from_model_sheet_names_option_contains_invalid_character(
    invalid_character: str,
) -> None:
    # Act & assert.
    with pytest.raises(
        SerializationError,
        match=(
            r"'CustomSheetName.*' is not a valid Excel sheet name "
            r"\(it contains invalid characters: '.*'\)"
        ),
    ):
        serialize(
            "xlsx",
            [],
            model_sheet_names={
                "tests.DummyModel": f"CustomSheetName{invalid_character}",
            },
        )


@pytest.mark.django_db()
def test_serializer_removes_sheets_not_added_by_itself() -> None:
    # Arrange.
    obj_1 = DummyModel._default_manager.create()
    obj_2 = DummyModel._default_manager.create()

    # Act.
    wb = serialize("xlsx", [obj_1, obj_2])

    # Assert.
    assert wb.sheetnames == ["tests.DummyModel"]
