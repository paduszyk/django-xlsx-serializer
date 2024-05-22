from __future__ import annotations

from django.db import models


class DummyModel(models.Model):
    pass


class DummyModelA(models.Model):
    pass


class DummyModelB(models.Model):
    pass


class BlankFieldModel(models.Model):
    blank_field = models.CharField(max_length=255, blank=True)


class NullFieldModel(models.Model):
    null_field = models.IntegerField(null=True)


class NotNullFieldModel(models.Model):
    not_null_field = models.IntegerField(null=False)


class LabelLongerThan31CharactersModel(models.Model):
    pass


class LabelLongerThan31CharactersModelA(models.Model):
    pass


class LabelLongerThan31CharactersModelB(models.Model):
    pass
