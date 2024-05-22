from __future__ import annotations

from django.db import models


class PrimaryKeyModel(models.Model):
    pass


class NaturalKeyModelManager(models.Manager["NaturalKeyModel"]):
    def get_by_natural_key(
        self,
        nk_field_1: str,
        nk_field_2: int,
    ) -> NaturalKeyModel:
        return self.get(nk_field_1=nk_field_1, nk_field_2=nk_field_2)


class NaturalKeyModel(models.Model):
    nk_field_1 = models.CharField(max_length=255)
    nk_field_2 = models.IntegerField()

    objects = NaturalKeyModelManager()

    class Meta:
        unique_together = (("nk_field_1", "nk_field_2"),)

    def natural_key(self) -> tuple[str, int]:
        return (self.nk_field_1, self.nk_field_2)


class ForeignKeyModel(models.Model):
    to_pk_model_field = models.ForeignKey(
        "tests.PrimaryKeyModel",
        on_delete=models.CASCADE,
        related_name="+",
    )
    to_nk_model_field = models.ForeignKey(
        "tests.NaturalKeyModel",
        on_delete=models.CASCADE,
        related_name="+",
    )


class OneToOneFieldModel(models.Model):
    to_pk_model_field = models.OneToOneField(
        PrimaryKeyModel,
        on_delete=models.CASCADE,
        related_name="+",
    )
    to_nk_model_field = models.OneToOneField(
        NaturalKeyModel,
        on_delete=models.CASCADE,
        related_name="+",
    )


class ManyToManyFieldModel(models.Model):
    to_pk_model_field = models.ManyToManyField(PrimaryKeyModel, related_name="+")
    to_nk_model_field = models.ManyToManyField(NaturalKeyModel, related_name="+")
