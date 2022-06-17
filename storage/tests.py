from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from storage.models import Client


class ClientTests(APITestCase):
    def test_get_data(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('api:is_exist')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Client.objects.count(), 0)

    # def test_create_new_client(self):
    #     """
    #     Ensure we can create a new account object.
    #     """
    #     url = reverse('is_exist')
    #     data = {'name': 'DabApps'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Client.objects.count(), 1)
    #     self.assertEqual(Client.objects.get().name, 'DabApps')