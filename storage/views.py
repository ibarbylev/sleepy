from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer


def index_view(request):
    return render(request, 'storage/index.html')


# class ClientList(generics.CreateAPIView):
class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def get(self, request, *args, **kwargs):
    #     return Response(f"forbidden request!")

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client_n = serializer.validated_data['client_name']
            client_d_cr = serializer.validated_data['createdAt']

            clients = Client.objects.filter(client_name=client_n)
            if clients:
                client_from_db = clients.first()
                client_nn = client_from_db.client_name
                client_date_reg = client_from_db.createdAt
                if client_nn == client_n and client_date_reg == client_d_cr:
                    return Response(f"Client ID is exist")
            else:
                serializer.save()
                last_client = Client.objects.all().last()
                return Response(f"ID: {last_client.pk}")

        return Response(f"Error of data validation: {serializer.errors}")


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientAddSleeps(generics.RetrieveUpdateAPIView):
    """
    Add sleeps to client
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            pass


"""
http://127.0.0.1:8000/api/is_exist/
    {
        "id": 2,
        "client_name": "aaaB",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "sleeps": [
            {
                "id": 3,
                "segments": [
                    {
                        "id": 1,
                        "start": "2022-04-09T15:18:39+03:00",
                        "finish": "2022-04-09T15:18:41+03:00",
                        "length": 1,
                        "lengthHM": "0:01"
                    }
                ],
                "startRoutineTime": "2022-04-08T05:06:26+03:00",
                "startFallingAsleepTime": "2022-04-08T05:06:28+03:00",
                "finishTime": "2022-04-08T05:06:56+03:00",
                "isItNightSleep": false,
                "place": "Place 3",
                "moodStartOfSleep": "Place 3",
                "moodEndOfSleep": "Place 3"
            },
            {
                "id": 4,
                "segments": [
                    {
                        "id": 1,
                        "start": "2022-04-09T15:18:39+03:00",
                        "finish": "2022-04-09T15:18:41+03:00",
                        "length": 1,
                        "lengthHM": "0:01"
                    },
                    {
                        "id": 2,
                        "start": "2022-04-09T15:35:44+03:00",
                        "finish": "2022-04-09T15:35:47+03:00",
                        "length": 3,
                        "lengthHM": "00:03"
                    }
                ],
                "startRoutineTime": "2022-04-08T05:09:10+03:00",
                "startFallingAsleepTime": "2022-04-08T05:09:11+03:00",
                "finishTime": "2022-04-08T05:09:14+03:00",
                "isItNightSleep": false,
                "place": "Place 4",
                "moodStartOfSleep": "Place 4",
                "moodEndOfSleep": "Place 4"
            }
        ]
    }
"""