from __future__ import annotations

from django.db import models


class EmailFieldModel(models.Model):
    email_field = models.EmailField()


class GenericIPAddressFieldModel(models.Model):
    generic_ip_address_field = models.GenericIPAddressField()


class JSONFieldModel(models.Model):
    json_field = models.JSONField()


class URLFieldModel(models.Model):
    url_field = models.URLField()


class UUIDFieldModel(models.Model):
    uuid_field = models.UUIDField()
