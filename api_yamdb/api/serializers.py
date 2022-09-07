from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для объектов модели Category."""

    class Meta:
        fields = ["name", "slug", ]
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для объектов модели Genre."""

    class Meta:
        fields = ["name", "slug", ]
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения списка объектов модели Title."""

    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )

    class Meta:
        fields = ["name", "year", "genre", "category", ]
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения объекта модели Title."""

    genre = GenreSerializer()
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        fields = ["id", "name", "year", "description", "rating", "genre",
                  "category", ]
