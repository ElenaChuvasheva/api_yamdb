from rest_framework import serializers


def validate_username_not_me(value):
    if value == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать \'me\' в качестве юзернейма'
        )
