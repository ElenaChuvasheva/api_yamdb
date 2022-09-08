from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAnonymous
from .serializers import (CommentSerializer, JWTTokenSerializer,
                          ReviewSerializer)
from api.serializers import CustomUserSerializer, SignupSerializer
from reviews.models import Review, Title
from users.models import CustomUser


# не доделано - без авторизации толком не потестить
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    # permission_classes = (permissions.IsAuthenticated,)

#    def perform_create(self, serializer):
#        serializer.save(author=self.request.user)
    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(title=get_object_or_404(Title, pk=title_id))


# тоже не доделано из-за отсутствия авторизации
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(review=get_object_or_404(Review, pk=review_id))


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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({"token": str(token)}, status=status.HTTP_200_OK)
