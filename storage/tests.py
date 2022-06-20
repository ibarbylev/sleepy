import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from storage.models import Client, Sleep, Segment


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
        data_3 = """{
            "id": 2,
            "client_name": "aaaB",
            "birthdate": "2021-11-09T14:00:00+02:00",
            "createdAt": "2021-11-09T14:00:11+02:00",
            "consultant": null,
            "sleeps": []
        }"""
        response = self.client.post(url, json.loads(data_3), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"id":2}')
        self.assertEqual(Client.objects.count(), 2)

        # 4. user with other name
        data_4 = """{
            "id": 2,
            "client_name": "aaaC",
            "birthdate": "2021-11-09T14:00:00+02:00",
            "createdAt": "2021-11-09T14:00:00+02:00",
            "consultant": null,
            "sleeps": []
        }"""
        response = self.client.post(url, json.loads(data_4), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"id":3}')
        self.assertEqual(Client.objects.count(), 3)


class TestRequestAPIaddSleeps(APITestCase):
    """Testing usl 'api/add-sleeps"""

    def test_get_request(self):
        """Get request create nothing"""
        url = reverse('api:add_sleeps', args=(1,))

        # 1. request with empty DB
        response = self.client.get(url, format='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Sleep.objects.count(), 0)
        self.assertEqual(response.content, b'{"detail":"Not found."}')

    def test_post_request(self):
        url = reverse('api:add_sleeps', args=(1,))

        # first add new client
        data_sleep = """
    {
        "id": 2,
        "client_name": "aaaB",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "consultant": null,
        "sleeps": [
            {
                "id": 3,
                "locked": true,
                "note": null,
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
                "locked": true,
                "note": null,
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

        # 1. Trying to add a sleep to a non-existent client
        response = self.client.put(url, json.loads(data_sleep), format='json')
        self.assertEqual(Client.objects.count(), 0)
        self.assertEqual(Sleep.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,  b'"Client not found!"')

        # 2. Creating a new client and adding dreams to it
        # -- add Client 1
        Client.objects.create(
            client_name='aaaB',
            birthdate='2021-11-09T14:00:00+02:00',
            createdAt='2021-11-09T14:00:00+02:00',
        )
        # -- add Client 2
        Client.objects.create(
            client_name='aaaA',
            birthdate='2021-11-09T14:00:00+02:00',
            createdAt='2021-11-09T14:00:00+02:00',
        )
        self.assertEqual(Client.objects.count(), 2)
        # -- add sleeps to Client 2
        response = self.client.put(url, json.loads(data_sleep), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sleep.objects.count(), 2)
        self.assertEqual(Segment.objects.count(), 3)
        RESPONSE_CONTENT = b'{"id":1,"client_name":"aaaB","birthdate":"2021-11-09T14:00:00+02:00",' \
            b'"createdAt":"2021-11-09T14:00:00+02:00","consultant":null,"sleeps":[{"id":1,' \
            b'"segments":[{"id":1,"start":"2022-04-09T15:18:39+03:00",' \
            b'"finish":"2022-04-09T15:18:41+03:00","length":1,"lengthHM":"0:01"}],' \
            b'"locked":true,"note":null,"startRoutineTime":"2022-04-08T05:06:26+03:00",' \
            b'"startFallingAsleepTime":"2022-04-08T05:06:28+03:00",' \
            b'"finishTime":"2022-04-08T05:06:56+03:00","isItNightSleep":false,"place":"Place 3",' \
            b'"moodStartOfSleep":"Place 3","moodEndOfSleep":"Place 3"},{"id":2,"segments":[{"id":2,' \
            b'"start":"2022-04-09T15:18:39+03:00","finish":"2022-04-09T15:18:41+03:00","length":1,' \
            b'"lengthHM":"0:01"},{"id":3,"start":"2022-04-09T15:35:44+03:00",' \
            b'"finish":"2022-04-09T15:35:47+03:00","length":3,"lengthHM":"00:03"}],"locked":true,' \
            b'"note":null,"startRoutineTime":"2022-04-08T05:09:10+03:00",' \
            b'"startFallingAsleepTime":"2022-04-08T05:09:11+03:00","finishTime":"2022-04-08T05:09:14+03:00",' \
            b'"isItNightSleep":false,"place":"Place 4","moodStartOfSleep":"Place 4","moodEndOfSleep":"Place 4"}]}'
        self.assertEqual(response.content,  RESPONSE_CONTENT)

        # 3. Add sleeps with only OLD data
        response = self.client.put(url, json.loads(data_sleep), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sleep.objects.count(), 2)
        self.assertEqual(Segment.objects.count(), 3)
        self.assertEqual(response.content,  RESPONSE_CONTENT)

        # 4. Add sleeps with new, but unlocked data
        data_sleep_new_unlocked = """
    {
        "id": 2,
        "client_name": "aaaB",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "consultant": null,
        "sleeps": [
            {
                "id": 3,
                "locked": false,
                "note": null,
                "segments": [
                    {
                        "id": 1,
                        "start": "2022-04-09T15:18:39+03:00",
                        "finish": "2022-04-09T15:18:41+03:00",
                        "length": 1,
                        "lengthHM": "0:01"
                    }
                ],
                "startRoutineTime": "2022-04-08T05:06:28+03:00",
                "startFallingAsleepTime": "2022-04-08T05:06:28+03:00",
                "finishTime": "2022-04-08T05:06:56+03:00",
                "isItNightSleep": false,
                "place": "Place 5",
                "moodStartOfSleep": "Place 5",
                "moodEndOfSleep": "Place 5"
            },
            {
                "id": 4,
                "locked": false,
                "note": null,
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
                "startRoutineTime": "2022-04-08T05:11:10+03:00",
                "startFallingAsleepTime": "2022-04-08T05:09:11+03:00",
                "finishTime": "2022-04-08T05:12:14+03:00",
                "isItNightSleep": false,
                "place": "Place 6",
                "moodStartOfSleep": "Place 6",
                "moodEndOfSleep": "Place 6"
            }
        ]
    }
"""
        response = self.client.put(url, json.loads(data_sleep_new_unlocked), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sleep.objects.count(), 2)
        self.assertEqual(Segment.objects.count(), 3)
        self.assertEqual(response.content,  RESPONSE_CONTENT)

        # 5. Add sleeps with new, but locked and unlocked data
        data_sleep_new_locked_unlocked = """
    {
        "id": 2,
        "client_name": "aaaB",
        "birthdate": "2021-11-09T14:00:00+02:00",
        "createdAt": "2021-11-09T14:00:00+02:00",
        "consultant": null,
        "sleeps": [
            {
                "id": 3,
                "locked": true,
                "note": null,
                "segments": [
                    {
                        "id": 1,
                        "start": "2022-04-09T15:18:39+03:00",
                        "finish": "2022-04-09T15:18:41+03:00",
                        "length": 1,
                        "lengthHM": "0:01"
                    }
                ],
                "startRoutineTime": "2022-04-08T05:06:28+03:00",
                "startFallingAsleepTime": "2022-04-08T05:06:28+03:00",
                "finishTime": "2022-04-08T05:06:56+03:00",
                "isItNightSleep": false,
                "place": "Place 5",
                "moodStartOfSleep": "Place 5",
                "moodEndOfSleep": "Place 5"
            },
            {
                "id": 4,
                "locked": true,
                "note": null,
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
                "startRoutineTime": "2022-04-08T05:11:10+03:00",
                "startFallingAsleepTime": "2022-04-08T05:09:11+03:00",
                "finishTime": "2022-04-08T05:12:14+03:00",
                "isItNightSleep": false,
                "place": "Place 6",
                "moodStartOfSleep": "Place 6",
                "moodEndOfSleep": "Place 6"
            }
        ]
    }
"""
        response = self.client.put(url, json.loads(data_sleep_new_locked_unlocked), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sleep.objects.count(), 4)
        self.assertEqual(Segment.objects.count(), 6)
        RESPONSE_CONTENT_2 = b'{"id":1,"client_name":"aaaB","birthdate":"2021-11-09T14:00:00+02:00"' \
                             b',"createdAt":"2021-11-09T14:00:00+02:00","consultant":null,"sleeps":' \
                             b'[{"id":1,"segments":[{"id":1,"start":"2022-04-09T15:18:39+03:00",' \
                             b'"finish":"2022-04-09T15:18:41+03:00","length":1,"lengthHM":"0:01"}],' \
                             b'"locked":true,"note":null,"startRoutineTime":"2022-04-08T05:06:26+03:00",' \
                             b'"startFallingAsleepTime":"2022-04-08T05:06:28+03:00",' \
                             b'"finishTime":"2022-04-08T05:06:56+03:00","isItNightSleep":false,' \
                             b'"place":"Place 3","moodStartOfSleep":"Place 3","moodEndOfSleep":"Place 3"},' \
                             b'{"id":2,"segments":[{"id":2,"start":"2022-04-09T15:18:39+03:00",' \
                             b'"finish":"2022-04-09T15:18:41+03:00","length":1,"lengthHM":"0:01"},' \
                             b'{"id":3,"start":"2022-04-09T15:35:44+03:00","finish":"2022-04-09T15:35:47+03:00",' \
                             b'"length":3,"lengthHM":"00:03"}],"locked":true,"note":null,' \
                             b'"startRoutineTime":"2022-04-08T05:09:10+03:00",' \
                             b'"startFallingAsleepTime":"2022-04-08T05:09:11+03:00",' \
                             b'"finishTime":"2022-04-08T05:09:14+03:00","isItNightSleep":false,"place":"Place 4",' \
                             b'"moodStartOfSleep":"Place 4","moodEndOfSleep":"Place 4"},{"id":3,' \
                             b'"segments":[{"id":4,"start":"2022-04-09T15:18:39+03:00",' \
                             b'"finish":"2022-04-09T15:18:41+03:00","length":1,"lengthHM":"0:01"}],' \
                             b'"locked":true,"note":null,"startRoutineTime":"2022-04-08T05:06:28+03:00",' \
                             b'"startFallingAsleepTime":"2022-04-08T05:06:28+03:00",' \
                             b'"finishTime":"2022-04-08T05:06:56+03:00","isItNightSleep":false,"place":"Place 5",' \
                             b'"moodStartOfSleep":"Place 5","moodEndOfSleep":"Place 5"},{"id":4,"segments":[{"id":5,' \
                             b'"start":"2022-04-09T15:18:39+03:00","finish":"2022-04-09T15:18:41+03:00","length":1,' \
                             b'"lengthHM":"0:01"},{"id":6,"start":"2022-04-09T15:35:44+03:00",' \
                             b'"finish":"2022-04-09T15:35:47+03:00","length":3,"lengthHM":"00:03"}],' \
                             b'"locked":true,"note":null,"startRoutineTime":"2022-04-08T05:11:10+03:00",' \
                             b'"startFallingAsleepTime":"2022-04-08T05:09:11+03:00",' \
                             b'"finishTime":"2022-04-08T05:12:14+03:00","isItNightSleep":false,"place":"Place 6",' \
                             b'"moodStartOfSleep":"Place 6","moodEndOfSleep":"Place 6"}]}'
        self.assertEqual(response.content,  RESPONSE_CONTENT_2)
