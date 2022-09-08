from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения объекта модели Title."""    

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


class TitleListSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения списка объектов модели Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        fields = ["id", "name", "year", "description", "rating", "genre",
                  "category", ]
        model = Title


# не закончено из-за авторизации
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if value > 10 or value <= 0:
            raise serializers.ValidationError('Проверьте оценку!')
        return value

#    def validate(self, data):
#        current_user = self.context['request'].user
#        if current_user.reviews:
#            raise serializers.ValidationError(
#                'Больше одного отзыва оставлять нельзя')
#        return data


# не закончено из-за авторизации
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = CustomUser
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'нельзя создать пользователя с именем \'me\''
            )
        return value

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
