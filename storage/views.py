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

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client_n = serializer.validated_data['client_name']
            client_d_cr = serializer.validated_data['createdAt']
            if Client.objects.filter(client_name=client_n) and Client.objects.filter(createdAt=client_d_cr):
                return Response(f"Client ID is exist")
            else:
                serializer.save()
                last_client = Client.objects.all().last()
                return Response(f"ID: {last_client.pk}")


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
