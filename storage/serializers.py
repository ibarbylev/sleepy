from datetime import datetime
from rest_framework import serializers, permissions

from storage.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name', 'birthdate', 'createdAt', 'sleeps']

    def validate_birthdate(self, value):
        """
        Check date between 01.01.2015 and 01.01.2052
        """
        if not value:
            raise serializers.ValidationError('birthdate must be date type!!!')

        past = datetime.fromisoformat("2015-01-01T00:00:00+01:00")
        future = datetime.fromisoformat("2052-01-01T00:00:00+01:00")
        if not (past < value < future):
            raise serializers.ValidationError('birthdate must be between 01.01.2015 and 01.01.2052')
        return value

    def validate_createdAt(self, value):
        """
        Check date between 01.01.2021 and 01.01.2052
        """
        if not value:
            raise serializers.ValidationError('createdAt must be date type!!!')

        past = datetime.fromisoformat("2021-01-01T00:00:00+01:00")
        future = datetime.fromisoformat("2052-01-01T00:00:00+01:00")
        if not (past < value < future):
            raise serializers.ValidationError('createdAt must be between 01.01.2021 and 01.01.2052')
        return value

    # def validate(self, attrs):
    #     """
    #     If client_name
    #     """
    #     if attrs:
    #         raise serializers.ValidationError("Ошибка валидации!!!")
    #     return attrs
