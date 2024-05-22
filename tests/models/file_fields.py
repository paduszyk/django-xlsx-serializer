from __future__ import annotations

from django.db import models


class FileFieldModel(models.Model):
    file_field = models.FileField()


class ImageFieldModel(models.Model):
    image_field = models.ImageField()


class FilePathFieldModel(models.Model):
    file_path_field = models.FilePathField()
