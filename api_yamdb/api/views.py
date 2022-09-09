
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, pagination, permissions,
                            serializers, status, viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsAnonymous,
                             IsEditorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             CustomUserSerializer, GenreSerializer,
                             JWTTokenSerializer, ReviewSerializer,
                             SignupExistingSerializer, SignupSerializer,
                             TitleListSerializer, TitleSerializer,
                             UserEditSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):

    """
    Пользовательский класс вьюсета.
    Создает и удаляет объект и возвращет список объектов.
    """

    pass


class CategoryViewSet(CreateListDestroyViewSet):

    """Вьюсет для выполнения операций с объектами модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):

    """Вьюсет для выполнения операций с объектами модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):

    """Вьюсет для выполнения операция с объектами модели Title."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('-year')
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsEditorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title, pk=title_id))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsEditorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user,
                        review=get_object_or_404(Review, pk=review_id))


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    pagination_class = pagination.PageNumberPagination

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def send_confirmation_code(username):
    user = CustomUser.objects.get(username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения, {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


@api_view(['POST'])
@permission_classes([IsAnonymous])
def signup(request):
    username = request.data.get('username')
    user_exists = CustomUser.objects.filter(username=username).exists()
    if user_exists:
        serializer = SignupExistingSerializer(data=request.data)
    else:
        serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        raise serializers.ValidationError(serializer.errors)
    if not user_exists:
        serializer.save()
    send_confirmation_code(username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAnonymous])
def get_auth_token(request):
    serializer = JWTTokenSerializer(data=request.data)
    if not serializer.is_valid():
        raise serializers.ValidationError(serializer.errors)
    user = get_object_or_404(
        CustomUser,
        username=request.data.get('username')
    )
    if not default_token_generator.check_token(
        user, request.data.get('confirmation_code')
    ):
        err = 'Пароль не совпадает с отправленным на email'
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
