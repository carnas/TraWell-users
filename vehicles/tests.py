from django.test import TestCase
from vehicles.factories import VehicleFactory
from users.factories import UserFactory
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

import json

AUTH_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJVWUxwNjc4ZWkzcm1xQ0Y0VHV5TGZBSUg2WDFnTURkSFIzWkZpSjlPS1Q0In0.eyJleHAiOjE2NjYzNjAyNjQsImlhdCI6MTY2NjM1OTk2NCwiYXV0aF90aW1lIjoxNjY2MzU5OTYzLCJqdGkiOiI5YTM5MmNhNy0zZjE5LTQzNjgtODI1Ny0xMWNhOTAyNzdlM2MiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0Ojg0MDMvYXV0aC9yZWFsbXMvVHJhV2VsbCIsImF1ZCI6WyJzb2NpYWwtb2F1dGgiLCJyZWFsbS1tYW5hZ2VtZW50IiwicmVhY3QiLCJhY2NvdW50Il0sInN1YiI6IjY1ODMwOWYxLTdiZmMtNDcxYy05MmNhLTkzYTUwZjk2MmU2ZSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImtyYWtlbmQiLCJzZXNzaW9uX3N0YXRlIjoiZmJhM2M4NmUtYjUzMS00Yzk2LWIyYTctM2VkYTc0ZmVmZWFlIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vbG9jYWxob3N0OjkwMDAiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiYXBwLWFkbWluIiwidW1hX2F1dGhvcml6YXRpb24iLCJhcHAtdXNlciIsInByaXZhdGVfdXNlciIsImRlZmF1bHQtcm9sZXMtdHJhd2VsbCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InNvY2lhbC1vYXV0aCI6eyJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXX0sInJlYWxtLW1hbmFnZW1lbnQiOnsicm9sZXMiOlsidmlldy1pZGVudGl0eS1wcm92aWRlcnMiLCJ2aWV3LXJlYWxtIiwibWFuYWdlLWlkZW50aXR5LXByb3ZpZGVycyIsImltcGVyc29uYXRpb24iLCJyZWFsbS1hZG1pbiIsImNyZWF0ZS1jbGllbnQiLCJtYW5hZ2UtdXNlcnMiLCJxdWVyeS1yZWFsbXMiLCJ2aWV3LWF1dGhvcml6YXRpb24iLCJxdWVyeS1jbGllbnRzIiwicXVlcnktdXNlcnMiLCJtYW5hZ2UtZXZlbnRzIiwibWFuYWdlLXJlYWxtIiwidmlldy1ldmVudHMiLCJ2aWV3LXVzZXJzIiwidmlldy1jbGllbnRzIiwibWFuYWdlLWF1dGhvcml6YXRpb24iLCJtYW5hZ2UtY2xpZW50cyIsInF1ZXJ5LWdyb3VwcyJdfSwia3Jha2VuZCI6eyJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXX0sInJlYWN0Ijp7InJvbGVzIjpbImFkbWluIiwidXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6ImZiYTNjODZlLWI1MzEtNGM5Ni1iMmE3LTNlZGE3NGZlZmVhZSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1c2VyX3R5cGUiOiJQcml2YXRlIEFjY291bnQiLCJkYXRlX29mX2JpcnRoIjoiMjAwMC0wMy0wOSIsImZhY2Vib29rIjoiaHR0cHM6Ly9vcGVuLnNwb3RpZnkuY29tL2NvbGxlY3Rpb24vdHJhY2tzIiwibmFtZSI6Ik1vbmlrYSBHYWxpxYRza2EiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiIzbW9uaWthMTAwQGdtYWlsLmNvbSIsImluc3RhZ3JhbSI6IiIsImdpdmVuX25hbWUiOiJNb25pa2EiLCJmYW1pbHlfbmFtZSI6IkdhbGnFhHNrYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BTG01d3UxVlV1S3JQazdyeHJTRzdHQndWNXU1bHZqLUdZRFgzbEFHTzJCTj1zOTYtYyIsImVtYWlsIjoiM21vbmlrYTEwMEBnbWFpbC5jb20ifQ.SNJBOywc5PGuwkqJQztwdfeHEaLvJHVpHlJ8aEtFcLTOIP_HsaaLfjcPdIc2DAu4QhUaB1LCAIKCWsw6LJ9KQoraWY_oX3xV1AmByejnPb8emH-2KUqmx9MaYcTRNARlyyZsjtKBAd_Wj7b-7i758N7WNI26mRzeV0TQVk8PJ6bHZX3vIAprzzlHA8xUCNEHEj7AsTaOwNTkGH5KoCygPsP1ej8oKxwC72foTz9EBHPZrhdDIXVgTgZ255ONfTdq4dIIvlnHkSgnjt1fTaJ-5oE0qs6fVI0_7bk0qPEIHUjY31UB7pR9fdaaneEAUaJ-DswrhaRc3guuSvRPofZwiw"


class VehicleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_TOKEN)

    def test_get_user_vehicles_successful(self):
        user = UserFactory(email="3monika100@gmail.com")
        vehicle = VehicleFactory(user=user)
        response = self.client.get(f"/vehicles/user_vehicles/{user.user_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results[0]['make'], vehicle.make)

    def test_get_user_vehicles_not_allowed(self):
        user = UserFactory(email="lis@gmail.com")
        response = self.client.get(f"/vehicles/user_vehicles/{user.user_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(results, 'Not allowed')

    def test_post_user_vehicles_successful(self):
        user = UserFactory(email="3monika100@gmail.com")
        post_data = {'make': 'ford', 'model': 'mustang', 'color': 'black'}
        response = self.client.post(f"/vehicles/user_vehicles/{user.user_id}", data=post_data, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(results['make'], post_data['make'])

    def test_delete_user_vehicle_successful(self):
        user = UserFactory(email="3monika100@gmail.com")
        vehicle = VehicleFactory(user=user)
        response = self.client.delete(f"/vehicles/{vehicle.vehicle_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results, f"Car with id={vehicle.vehicle_id} deleted successfully")

    def test_delete_user_vehicle_not_belong_to_user(self):
        user = UserFactory(email="3monika100@gmail.com")
        user2 = UserFactory()
        vehicle = VehicleFactory(user=user2)
        response = self.client.delete(f"/vehicles/{vehicle.vehicle_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(results, f"Vehicle with id={vehicle.vehicle_id} does not belong to the user")

    def test_delete_user_vehicle_user_not_found(self):
        vehicle = VehicleFactory()
        response = self.client.delete(f"/vehicles/{vehicle.vehicle_id}")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(results, f"User not found")

    def test_delete_user_vehicle_not_found(self):
        user = UserFactory(email="3monika100@gmail.com")
        response = self.client.delete(f"/vehicles/1")
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(results, f"Car with id=1 not found")

    def test_patch_user_vehicle(self):
        user = UserFactory(email="3monika100@gmail.com")
        vehicle = VehicleFactory(user=user)
        patch_data = {'model': 'mustang'}
        response = self.client.patch(f"/vehicles/{vehicle.vehicle_id}", data=patch_data, format='json')
        results = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(results['model'], patch_data['model'])

