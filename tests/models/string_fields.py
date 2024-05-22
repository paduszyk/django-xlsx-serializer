from __future__ import annotations

from django.db import models


class CharFieldModel(models.Model):
    char_field = models.CharField(max_length=255)


class TextFieldModel(models.Model):
    text_field = models.TextField()


class SlugFieldModel(models.Model):
    slug_field = models.SlugField()
