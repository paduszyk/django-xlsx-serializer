from __future__ import annotations

from django.db import models


class AutoFieldModel(models.Model):
    auto_field = models.AutoField(primary_key=True)


class BigAutoFieldModel(models.Model):
    big_auto_field = models.BigAutoField(primary_key=True)


class SmallAutoFieldModel(models.Model):
    small_auto_field = models.SmallAutoField(primary_key=True)
