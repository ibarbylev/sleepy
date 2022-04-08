from datetime import datetime
from rest_framework import serializers, permissions

from storage.models import Client, Sleep


class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    sleeps = SleepSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'birthdate', 'createdAt', 'sleeps']

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
        print(value)
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


    # def update(self, client, validated_data):
    #     sleeps_data_list = validated_data.pop('sleeps')
    #     """
    #     [
    #         {
    #             "startRoutineTime":  "2022-03-22T13:13:28+01:00",
    #             "startFallingAsleepTime": "2022-03-22T13:13:28+01:00",
    #         },
    #         {
    #             "startRoutineTime":  "2022-03-22T13:13:28+01:00",
    #             "startFallingAsleepTime": "2022-03-22T13:13:28+01:00",
    #         },
    #     ]
    #     """
    #
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #
    #     profile.is_premium_member = profile_data.get(
    #         'is_premium_member',
    #         profile.is_premium_member
    #     )
    #     profile.has_support_contract = profile_data.get(
    #         'has_support_contract',
    #         profile.has_support_contract
    #      )
    #     profile.save()
    #
    #     return instance

