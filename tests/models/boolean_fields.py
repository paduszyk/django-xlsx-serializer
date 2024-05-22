from __future__ import annotations

from django.db import models


class BooleanFieldModel(models.Model):
    boolean_field = models.BooleanField()
