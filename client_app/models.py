from django.db import models
from server.models import Directory, Record


class Organization(Directory):
    address = models.CharField(
        verbose_name="Юр.Адрес",
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Client(Directory):
    organization = models.ForeignKey(
        Organization,
        verbose_name="Организация",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Pin(Record):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)
    code = models.CharField("Код", max_length=6)

    class Meta:
        verbose_name = "Пин-код"
        verbose_name_plural = "Пин-коды"

    def __str__(self) -> str:
        return f"{self.code} ({self.client})"
