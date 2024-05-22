from __future__ import annotations

from django.db import models


class IntegerFieldModel(models.Model):
    integer_field = models.IntegerField()


class BigIntegerFieldModel(models.Model):
    big_integer_field = models.BigIntegerField()


class SmallIntegerFieldModel(models.Model):
    small_integer_field = models.SmallIntegerField()


class PositiveIntegerFieldModel(models.Model):
    positive_integer_field = models.PositiveIntegerField()


class PositiveBigIntegerFieldModel(models.Model):
    positive_big_integer_field = models.PositiveBigIntegerField()


class PositiveSmallIntegerFieldModel(models.Model):
    positive_small_integer_field = models.PositiveSmallIntegerField()


class DecimalFieldModel(models.Model):
    decimal_field = models.DecimalField(max_digits=2, decimal_places=1)


class FloatFieldModel(models.Model):
    float_field = models.FloatField()
