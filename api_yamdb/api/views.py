from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, viewsets

from api.filters import TitleFilter
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleListSerializer, TitleSerializer)
from api.permissions import IsAdminOrReadOnly
from reviews.models import Category, Genre, Title


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Пользовательский класс вьюсета.
    Создает и удаляет объект и возвращет список объектов.
    """


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для выполнения операций с объектами модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ("name", )


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для выполнения операций с объектами модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ("name", )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для выполнения операция с объектами модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")
    )
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleListSerializer
        return TitleSerializer
