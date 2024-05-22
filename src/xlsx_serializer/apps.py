from __future__ import annotations

__all__ = [
    "XlsxSerializerConfig",
]

import sys

from django.apps import AppConfig
from django.core.serializers import register_serializer

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class XlsxSerializerConfig(AppConfig):
    name = "xlsx_serializer"

    @override
    def ready(self) -> None:
        super().ready()

        register_serializer("xlsx", "xlsx_serializer")
