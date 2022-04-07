from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models_old import Client
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

            client_from_db = Client.objects.filter(client_name=client_n).first()
            client_nn = client_from_db.client_name
            client_date_reg = client_from_db.createdAt
            if client_nn == client_n and client_date_reg == client_d_cr:
                return Response(f"Client ID is exist")
            else:
                serializer.save()
                last_client = Client.objects.all().last()
                return Response(f"ID: {last_client.pk}")

        return Response(f"Error of data validation!!!")


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
[
    {
        "id": 1,
        "client_name": "John Smith",
        "birthdate": "2022-04-04T03:07:30+03:00",
        "createdAt": "2022-04-04T03:07:34+03:00",
        "sleeps": null
    },
    {
        "id": 7,
        "client_name": "sdfg",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": null,
        "sleeps": null
    },
    {
        "id": 8,
        "client_name": "asdf",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": null,
        "sleeps": null
    },
    {
        "id": 9,
        "client_name": "asdf",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": null,
        "sleeps": null
    },
    {
        "id": 10,
        "client_name": "asg",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": null,
        "sleeps": null
    },
    {
        "id": 11,
        "client_name": "asdfasa",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "sleeps": null
    },
    {
        "id": 12,
        "client_name": "aaa",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "sleeps": null
    },
    {
        "id": 13,
        "client_name": "aaaA",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "sleeps": null
    },
    {
        "id": 14,
        "client_name": "aaaAAA",
        "birthdate": "2019-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "sleeps": null
    },
    {
        "id": 15,
        "client_name": "aaaAAA",
        "birthdate": "2019-11-09T14:00:00+02:00",
        "createdAt": "2022-11-09T14:00:00+02:00",
        "sleeps": null
    }
]
"""