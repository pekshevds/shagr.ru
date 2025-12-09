from transliterate import translit
from django.utils.text import slugify
from django.db import models
from server.models import Directory


class Category(Directory):
    slug = models.CharField(
        verbose_name="Ссылка",
        max_length=300,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
    parent = models.ForeignKey(
        "Category",
        verbose_name="Родитель",
        related_name="childs",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self) -> None:
        self.slug = slugify(translit(f"{self.name}", reversed=True))
        super().save()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Good(Directory):
    short_name = models.CharField(
        verbose_name="Короткое имя",
        max_length=50,
        blank=True,
        null=False,
        default="",
    )
    art = models.CharField(
        verbose_name="Артикул",
        max_length=50,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
    slug = models.CharField(
        verbose_name="Ссылка",
        max_length=300,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
    code = models.CharField(
        verbose_name="Код (1С)", max_length=11, blank=True, null=False, default=""
    )
    okei = models.CharField(
        verbose_name="Ед.", max_length=50, blank=True, null=False, default=""
    )
    balance = models.DecimalField(
        verbose_name="Остаток",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name="Описание", max_length=2048, blank=True, null=False, default=""
    )
    seo_title = models.TextField(
        verbose_name="<title>", null=True, blank=True, default=""
    )
    seo_description = models.TextField(
        verbose_name="<description>",
        null=True,
        blank=True,
        default="",
    )
    seo_keywords = models.TextField(
        verbose_name="<keywords>",
        null=True,
        blank=True,
        default="",
    )

    def save(self) -> None:
        self.slug = slugify(translit(f"{self.name}-{self.art}", reversed=True))
        super().save()

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"
