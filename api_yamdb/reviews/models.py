from django.db import models

from reviews.validators import validate_year


class Category(models.Model):
    """
    Модель для создания категорий (типов) произведений.
    («Фильмы», «Книги», «Музыка»).
    """

    name = models.CharField(
        verbose_name="Название категории",
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Адрес категории",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для создания жанров."""
    name = models.CharField(
        verbose_name="Название категории",
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Адрес категории",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для создания произведений, к которым пишут отзывы."""

    name = models.CharField(
        verbose_name="Название произведения",
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
        validators=[validate_year, ]
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        related_name='title_genre',
    )
    category = models.ForeignKey(
        Category,
        related_name="category",
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Название произведения"
        verbose_name_plural = "Названия произведений"
        ordering = ("-year",)

    def __str__(self):
        return self.name
