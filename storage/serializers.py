from datetime import datetime
from rest_framework import serializers, permissions

from storage.models import Client, Sleep, Segment
from authentication.models import User


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = '__all__'


class SleepSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True)

    class Meta:
        model = Sleep
        fields = '__all__'


class ClientSerializerForReturnID(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        fields = ['id']


class ClientSerializer(serializers.ModelSerializer):
    sleeps = SleepSerializer(many=True, required=False, default=[])

    def create(self, validated_data):
        client = Client(
            client_name=validated_data.get('client_name'),
            birthdate=validated_data.get('birthdate'),
            createdAt=validated_data.get('createdAt'),
            )
        client.save()
        return client
    # def create(self, validated_data):
    #     sleeps_data = validated_data.pop('sleeps')
    #     sleeps = []
    #     if sleeps_data:
    #         for sleep_data in sleeps_data:
    #             print(sleep_data)
    #             sleep = Sleep(
    #                 startRoutineTime=sleep_data.get('startRoutineTime'),
    #                 startFallingAsleepTime=sleep_data.get('startFallingAsleepTime'),
    #                 finishTime=sleep_data.get('finishTime'),
    #                 isItNightSleep=sleep_data.get('isItNightSleep', False),
    #                 place=sleep_data.get('place'),
    #                 moodStartOfSleep=sleep_data.get('moodStartOfSleep'),
    #                 moodEndOfSleep=sleep_data.get('moodEndOfSleep')
    #             )
    #             sleep.save()
    #
    #             segments_data = sleep_data.pop('segments')
    #             if segments_data:
    #                 segments = []
    #                 for segment_data in segments_data:
    #                     segment = Segment(
    #                         start=segment_data.get('start'),
    #                         finish=segment_data.get('finish'),
    #                         length=segment_data.get('length'),
    #                         lengthHM=segment_data.get('lengthHM')
    #                     )
    #                     segment.save()
    #                     segments.append(segment)
    #
    #                 sleep.segments.set(segments)
    #                 sleep.save()
    #
    #             sleeps.append(sleep)
    #
    #     client = Client(
    #         client_name=validated_data.get('client_name'),
    #         birthdate=validated_data.get('birthdate'),
    #         createdAt=validated_data.get('createdAt'),
    #     )
    #     client.save()
    #     client.sleeps.set(sleeps)
    #
    #     client.save()
    #     return client

    def update(self, instance, validated_data):
        sleeps_data = validated_data.pop('sleeps')
        sleeps = []
        if sleeps_data:
            for sleep_data in sleeps_data:
                print(sleep_data)
                sleep = Sleep(
                    startRoutineTime=sleep_data.get('startRoutineTime'),
                    startFallingAsleepTime=sleep_data.get('startFallingAsleepTime'),
                    finishTime=sleep_data.get('finishTime'),
                    isItNightSleep=sleep_data.get('isItNightSleep', False),
                    place=sleep_data.get('place'),
                    moodStartOfSleep=sleep_data.get('moodStartOfSleep'),
                    moodEndOfSleep=sleep_data.get('moodEndOfSleep')
                )
                sleep.save()

                segments_data = sleep_data.pop('segments')
                if segments_data:
                    segments = []
                    for segment_data in segments_data:
                        segment = Segment(
                            start=segment_data.get('start'),
                            finish=segment_data.get('finish'),
                            length=segment_data.get('length'),
                            lengthHM=segment_data.get('lengthHM')
                        )
                        segment.save()
                        segments.append(segment)

                    sleep.segments.set(segments)
                    sleep.save()

                sleeps.append(sleep)

        client = instance
        client.sleeps.set(sleeps)

        client.save()
        return client

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'birthdate', 'createdAt', 'consultant', 'sleeps']

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


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
