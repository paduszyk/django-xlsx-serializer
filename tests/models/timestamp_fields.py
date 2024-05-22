from __future__ import annotations

from django.db import models


class DateFieldModel(models.Model):
    date_field = models.DateField()


class TimeFieldModel(models.Model):
    time_field = models.TimeField()


class DateTimeFieldModel(models.Model):
    datetime_field = models.DateTimeField()


class DurationFieldModel(models.Model):
    duration_field = models.DurationField()
