from django.db import models

from reviews.validators import validate_year
from users.models import CustomUser


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


class Review(models.Model):
    """Модель для отзыва."""
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    score = models.IntegerField(verbose_name='Оценка')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='unique_author_title'),
        )


class Comment(models.Model):
    """Модель для комментария к отзыву."""
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
