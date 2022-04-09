from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer


def index_view(request):
    return render(request, 'storage/index.html')


def check_is_client_exists(serializer, pk=None):
    """
    Check if client exists by name, date of create account and pk(optional)
    """

    client_n = serializer.validated_data['client_name']
    client_d_cr = serializer.validated_data['createdAt']

    client = Client.objects.filter(client_name=client_n)
    if client:
        client_from_db = client.first()
        client_nn = client_from_db.client_name
        client_date_reg = client_from_db.createdAt
        if client_nn == client_n and client_date_reg == client_d_cr:
            if pk is None:
                return True
            else:
                if client.pk == pk:
                    return True


# class ClientList(generics.CreateAPIView):
# TODO change ListCreateAPIView to CreateAPIView
class ClientIsExists(generics.ListCreateAPIView):
    """
    Check the client by name, birthdate and date of create account
    (POST request with JSON with fields:
        1. client_name
        2. birthdate
        3. createdAt)
    If exists --> return "Client ID is exist"
    If doesn't -->
        1. Create a new client
        2. Return client id
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            if check_is_client_exists(serializer):
                return Response(f"Client ID is exist")
            else:
                serializer.save()
                new_created_client = Client.objects.all().last()
                return Response(f"ID: {new_created_client.pk}")

        return Response(f"Error of data validation: {serializer.errors}")


# class ClientList(generics.CreateAPIView):
# TODO change ListCreateAPIView to CreateAPIView
class ClientList(generics.ListCreateAPIView):
    """
    Add new client by new name and date of create account
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def get(self, request, *args, **kwargs):
    #     return Response(f"forbidden request!")

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client_n = serializer.validated_data['client_name']
            client_d_cr = serializer.validated_data['createdAt']

            client = Client.objects.filter(client_name=client_n)
            if client:
                client_from_db = client.first()
                client_nn = client_from_db.client_name
                client_date_reg = client_from_db.createdAt
                if client_nn == client_n and client_date_reg == client_d_cr:
                    return Response(f"Client ID is exist")
            else:
                serializer.save()
                last_client = Client.objects.all().last()
                return Response(f"ID: {last_client.pk}")

        return Response(f"Error of data validation: {serializer.errors}")


# class ClientDeleteClientSleeps(generics.UpdateAPIView):
# TODO change RetrieveUpdateAPIView to UpdateAPIView
class ClientDeleteClientSleeps(generics.RetrieveUpdateAPIView):
    """
    Delete all sleeps and its dependent segments for signed client
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, pk, *args, **kwargs):
        print('pk =', pk)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        if Client.objects.filter(pk=pk):
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(client, data=request.data)
            if serializer.is_valid():
                client_n = serializer.validated_data['client_name']
                if client_n != client.client_name:
                    return Response(f"Error in name for client.id={pk}")

                [sg.delete() for sleep in client.sleeps.all() for sg in sleep.segments.all()]
                [sleep.delete() for sleep in client.sleeps.all()]

            return self.update(request, *args, **kwargs)

        return Response("Client doesn't exist!")


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
