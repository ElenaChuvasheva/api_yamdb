from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOrReadOnly, IsAnonymous, IsEditorOrReadOnly
from .serializers import (CommentSerializer, JWTTokenSerializer,
                          ReviewSerializer)
from api.serializers import (CategorySerializer, CustomUserSerializer,
                             SignupSerializer)
from reviews.models import Category, Review, Title
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
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
    http_method_names = ['get', 'post', 'patch', 'delete']
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
    permission_classes = ()


def create_and_send_confirmation_code(username):
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
    serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        raise serializers.ValidationError(serializer.errors)
    serializer.save()
    username = request.data.get('username')
    create_and_send_confirmation_code(username)
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
    return Response({"token": str(token)}, status=status.HTTP_200_OK)
