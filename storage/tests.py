import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from storage.models import Client


class TestRequestAPIisExist(APITestCase):
    """Testing usl 'api/is_exist"""
    def test_get_request(self):
        """Get request create nothing"""
        url = reverse('api:is_exist')
        response = self.client.get(url, format='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 0)

    def test_post_request(self):
        url = reverse('api:is_exist')
        data = """{
            "id": 2,
            "client_name": "aaaB",
            "birthdate": "2021-11-09T14:00:00+02:00",
            "createdAt": "2021-11-09T14:00:00+02:00",
            "consultant": null,
            "sleeps": []
        }"""
        # creating new user
        response = self.client.post(url, json.loads(data), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"id":1}')
        self.assertEqual(Client.objects.count(), 1)

        # 1. user with these parameters already exists
        response = self.client.post(url, json.loads(data), format='json')
        self.assertEqual(response.content, b'"Client ID is exist"')

        # 2. user with same name but diff birthdate
        data_2 = """{
            "id": 2,
            "client_name": "aaaB",
            "birthdate": "2021-11-09T14:00:11+02:00",
            "createdAt": "2021-11-09T14:00:00+02:00",
            "consultant": null,
            "sleeps": []
        }"""
        response = self.client.post(url, json.loads(data_2), format='json')
        self.assertEqual(response.content, b'"Client ID is exist"')
        self.assertEqual(Client.objects.count(), 1)

        # 3. user with same name but diff createdAt
        data_2 = """{
            "id": 2,
            "client_name": "aaaB",
            "birthdate": "2021-11-09T14:00:00+02:00",
            "createdAt": "2021-11-09T14:00:11+02:00",
            "consultant": null,
            "sleeps": []
        }"""
        response = self.client.post(url, json.loads(data_2), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"id":2}')
        self.assertEqual(Client.objects.count(), 2)

        # 4. user with other name
        data_2 = """{
            "id": 2,
            "client_name": "aaaC",
            "birthdate": "2021-11-09T14:00:00+02:00",
            "createdAt": "2021-11-09T14:00:00+02:00",
            "consultant": null,
            "sleeps": []
        }"""
        response = self.client.post(url, json.loads(data_2), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"id":3}')
        self.assertEqual(Client.objects.count(), 3)

