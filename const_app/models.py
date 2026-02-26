from django.db import models
from server.models import Record, Directory


class Vat(Directory):
    value = models.DecimalField(
        verbose_name="Значение",
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        default=0,
    )

    class Meta:
        verbose_name = "Ставка НДС"
        verbose_name_plural = "Ставки НДС"


class Const(Record):
    start = models.DateTimeField(verbose_name="Период")
    vat = models.ForeignKey(
        Vat,
        verbose_name="Ставка НДС",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Константа"
        verbose_name_plural = "Константы"
