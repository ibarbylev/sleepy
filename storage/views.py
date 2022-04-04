from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer


def index_view(request):
    return render(request, 'storage/index.html')


# class ClientList(generics.CreateAPIView):
class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def post(self, request, *args, **kwargs):
    #     print('request', request)
    #     print('args', args)
    #     print('kwargs', kwargs)
    #     # if True:
    #     #     self.create(request, *args, **kwargs)
    #     #     return Response('hi')
    #     return Response(f"request: {request}, args: {args}, kwargs: {kwargs}")


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
