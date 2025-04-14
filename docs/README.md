# django-xlsx-serializer

[![PyPI: Version](https://img.shields.io/pypi/v/django-xlsx-serializer?style=flat-square&logo=pypi&logoColor=white)][pypi]
[![PyPI: Python](https://img.shields.io/pypi/pyversions/django-xlsx-serializer?style=flat-square&logo=python&logoColor=white)][pypi]
[![PyPI: Django](https://img.shields.io/pypi/djversions/django-xlsx-serializer?style=flat-square&color=0C4B33&label=django&logo=django)][pypi]
[![PyPI: License](https://img.shields.io/pypi/l/django-xlsx-serializer?style=flat-square)][pypi]

[![Pre-commit](https://img.shields.io/github/actions/workflow/status/paduszyk/django-xlsx-serializer/pre-commit-run.yml?style=flat-square&label=pre-commit&logo=pre-commit)][pre-commit]
[![Python: CI](https://img.shields.io/github/actions/workflow/status/paduszyk/django-xlsx-serializer/python-ci.yml?style=flat-square&logo=github&label=CI)][python-ci]
[![Codecov](https://img.shields.io/codecov/c/github/paduszyk/django-xlsx-serializer?style=flat-square&logo=codecov)][codecov]

[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg?style=flat-square)][nox]
[![Ruff](https://img.shields.io/endpoint?style=flat-square&url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)][ruff]
[![Mypy](https://img.shields.io/badge/type--checked-mypy-blue?style=flat-square&logo=python)][mypy]
[![Prettier](https://img.shields.io/badge/code%20style-prettier-1E2B33?style=flat-square&logo=Prettier)][prettier]
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-fa6673.svg?style=flat-square&logo=conventional-commits)][conventional-commits]

## Overview

`django-xlsx-serializer` is a [Django][django] application designed to handle
the data serialization and deserialization between Django models and Microsoft
Excel 2007+ workbooks. Utilizing the [OpenPyXL][openpyxl] engine, this tool
provides robust methods to export data from Django databases into XLSX files and
import data from the files back into the databases. This functionality is
essential for applications that require data exchange between Django-based
systems and Excel, facilitating such tasks as data migration, reporting, and
backups.

## Features

The app allows you to:

- Export Django models from a database to an Excel workbook via the
  [`dumpdata`][django-dumpdata] command.
- Populate databases from Excel fixtures using the [`loaddata`][django-loaddata]
  command.
- Interact with Excel workbooks (either files or `openpyxl.Workbook` objects)
  and the database using the Django's core [serialization][django-serialization]
  utilities.

## Requirements

| Python | Django                            | Database engines    |
| :----- | :-------------------------------- | :------------------ |
| 3.9    | 3.2, 4.0, 4.1, 4.2                | SQLite3, PostgreSQL |
| 3.10   | 3.2, 4.0, 4.1, 4.2, 5.0, 5.1, 5.2 | SQLite3, PostgreSQL |
| 3.11   | 4.1, 4.2, 5.0, 5.1, 5.2           | SQLite3, PostgreSQL |
| 3.12   | 4.2, 5.0, 5.1, 5.2                | SQLite3, PostgreSQL |
| 3.13   | 5.1, 5.2                          | SQLite3, PostgreSQL |

All setups require OpenPyXL < 4.

## Installation

The fastest way to add the package to your Python environment is to download and
install it directly from [PyPI][pypi]. Use `pip`:

```console
pip install django-xlsx-serializer
```

or any other dependency manager of your preference.

As soon as the installation is completed, all the app's functionalities can be
accessed from the `xlsx_serializer` module:

```python
import xlsx_serializer
```

> The app is compatible with Excel 2007+ XLSX workbooks only. Adding support for
> the older XLS format is not planned.

## Django Configuration

The app utilities can be incorporated into your Django project by following one
of the approaches listed below:

1. Installing the package as an app.
2. Adding the package to serialization modules.
3. Registering the app's serializers module from another app.

All of them associate the app's serializer with the `xlsx` format.

### Install as an App

In your project settings module add `xlsx_serializers` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "xlsx_serializer",
    # ...
]
```

### Add to Serialization Modules

In your project settings module update the `SERIALIZATION_MODULES` dictionary:

```python
SERIALIZATION_MODULES = {
    # ...
    "xlsx": "xlsx_serializer",
    # ...
}
```

### Register from Another App

In any of the apps installed in your projects (let us call it `myapp`), register
the `xlsx_serializer` manually in the app's `ready` hook:

```python
# myapp/apps.py

from django.apps import AppConfig
from django.core import serializers


class MyAppConfig(AppConfig):
    name = "myapp"

    def ready(self) -> None:
        super().ready()

        # ...

        # Register serializers.
        serializers.register_serializer("xlsx", "xlsx_serializer")
```

> There are many Django projects using a "core" app for defining project-wide
> utilities (e.g., custom commands, template tags, etc.). The configuration
> class of such an app is a good place to apply the code snippet above.

## Usage

### Excel Workbooks vs. Django Models

The app adopts quite intuitive correspondence between Excel workbooks (i.e., the
collections of worksheets) and Django models:

- A Django model is represented by a single worksheet.
- In an Excel workbook, the models are identified by worksheet names.
- Within an Excel worksheet, model instances are represented by rows, while the
  columns correspond to the model's fields.

### Serialization

Serialization can be run either by the built-in [`dumpdata`][django-dumpdata]
Django management command:

```console
python manage.py dumpdata --format xlsx --output dump.xlsx
```

or from Django interactive shell:

```python
>>> from django.core import serializers
>>> from polls.models import Question
>>> serializers.serialize("xlsx", Question.objects.all(), output="dump.xlsx")
# Prints: <openpyxl.workbook.workbook.Workbook object at ...>
```

Both the command and expression shown above save `dump.xlsx` workbook file. The
latter additionally returns an `openpyxl.Workbook` object, which can be used
later if necessary (e.g., in development or maintenance scripts).

When serializing, the app creates worksheets named using fully qualified model
labels. For example, the `Question` model defined in the `polls` app is
serialized to the "polls.Question" worksheet. Excel does not accept worksheet
names longer than 31 characters. If the model's label is longer, it's truncated.
A useful feature allowing you to circumvent this issue is that the output
worksheet names can be customized using the `model_sheet_names` option. So, the
command:

```python
>>> workbook = serialize(
        "xlsx",
        Question.objects.all(),
        model_sheet_names={"polls.Question": "Questions"},
    )
>>> workbook
# Prints: <openpyxl.workbook.workbook.Workbook object at ...>
```

results in the `polls.Question` model data serialized in the "Questions"
worksheet. Note that this option is not available when using the app via the
`dumpdata` command.

> The app inspects each key and value of the `model_sheet_names` dictionary. For
> the keys, it validates whether they represent valid model identifiers. The
> values, in turn, are checked to see if they are unique, are not too long, and
> do not contain invalid characters (`?`, `*`, `:`, `\`, `/`, `[`, `]`).

Other key points:

- `DateField`, `DateTimeField`, and `TimeField` values are serialized as
  ISO 8601 strings.
- `JSONField` values are serialized as JSON strings returned by the respective
  field's encoders.
- `ManyToManyField` values are serialized as stringified lists of foreign keys.
- The app supports serialization by using natural keys. If it is triggered (by
  applying the `--natural-primary`/`--natural-foreign` flags), the natural keys
  are serialized as stringified tuples (or their lists in the case of
  many-to-many relations).

### Deserialization

The recommended way of employing the app to load the model data from an Excel
fixture to the database is to call it via the [`loaddata`][django-loaddata]
command:

```console
python manage.py loaddata fixture.xlsx
```

Deserialization requires the input workbook's worksheets to have names that are
either the fully qualified labels or model names (case-insensitive). The latter
can be applied if the model name is unique. For example, if the project uses
models `polls.Question` and `exams.Question`, the worksheet named "Question"
will not be deserialized.

Within a worksheet, ensure that the column headers correspond to the field names
of the respective model. The app ignores a column if it does not represent
a field. Empty rows and columns surrounding the data range are ignored as well.
However, the app does not check the data for the missing or invalid values.

Other key points:

- Populating `DateField`, `DateTimeField`, and `TimeField` with timezone support
  enabled in Django settings requires date/time values to be saved as ISO 8601
  strings (date/time type values in Excel don't store timezone information).
- Deserializing `JSONfield` requires values in a format compatible with the JSON
  decoder of the respective field.
- In the case of `ManyToManyField` provide string representations of Python
  lists containing the primary (or natural, see the next bullet) keys of the
  related objects.
- The app handles deserialization from natural keys by using `ast.literal_eval`.
  Make sure to provide the keys that are valid string representations of the
  corresponding values (i.e., tuples of primitive Python literals; in most
  cases, they are strings &mdash; if so, use single quotes as text delimiters).

## Contributing

This is an open-source project that embraces contributions of all types. We
require all contributors to adhere to our [Code of Conduct][code-of-conduct].
For comprehensive instructions on how to contribute to the project, please refer
to our [Contributing Guide][contributing].

## Authors

Created and maintained by Kamil Paduszyński ([@paduszyk][paduszyk]).

## License

Released under the [MIT license][license].

[code-of-conduct]: https://github.com/paduszyk/django-xlsx-serializer/blob/main/docs/CODE_OF_CONDUCT.md
[codecov]: https://app.codecov.io/gh/paduszyk/django-xlsx-serializer
[contributing]: https://github.com/paduszyk/django-xlsx-serializer/blob/main/docs/CONTRIBUTING.md
[conventional-commits]: https://www.conventionalcommits.org/en/v1.0.0/
[django-dumpdata]: https://docs.djangoproject.com/en/5.0/ref/django-admin/#dumpdata
[django-loaddata]: https://docs.djangoproject.com/en/5.0/ref/django-admin/#loaddata
[django-serialization]: https://docs.djangoproject.com/en/5.0/topics/serialization/
[django]: https://www.djangoproject.com
[license]: https://github.com/paduszyk/django-xlsx-serializer/blob/main/LICENSE
[mypy]: https://mypy.readthedocs.io
[nox]: https://github.com/wntrblm/nox
[openpyxl]: https://openpyxl.readthedocs.io/en/stable/
[paduszyk]: https://github.com/paduszyk
[pre-commit]: https://github.com/paduszyk/django-xlsx-serializer/actions/workflows/pre-commit-run.yml
[prettier]: https://prettier.io
[pypi]: https://pypi.org/project/django-xlsx-serializer/
[python-ci]: https://github.com/paduszyk/django-xlsx-serializer/actions/workflows/python-ci.yml
[ruff]: https://docs.astral.sh/ruff/
