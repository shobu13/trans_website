import json

from django.forms import model_to_dict

import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.contrib.auth.models import User

from core.serializers import UserDetailSerializer, UserSerializer


class UserViewsetTest(APITestCase):
    """
    class de test des endpoints lié aux users.
    """

    @classmethod  # <- setUpClass doit être une méthode de classe, attention !
    def setUpTestData(cls):
        User.objects.create_superuser(username='admin', password='sysadmin', email='').save()

        user = User.objects.create_user('Shobu', 'shobu13@hotmail.fr', 'AzErTy#')
        user.last_name = 'Ser\'Hao'
        user.first_name = 'Shobu'
        user.street = '11 rue de la foucherais'
        user.city = 'vezin le coquet'
        user.postal_code = '35132'
        user.phone_number = '0620788001'
        user.birth_date = datetime.datetime.now().date()
        user.save()

        user2 = User.objects.create_user('Billy', 'Billy@hotmail.fr', 'AzErTy#')
        user2.last_name = 'Mitchell'
        user2.first_name = 'Billy'
        user2.street = '11 rue de la foucherais'
        user2.city = 'vezin le coquet'
        user2.postal_code = '35132'
        user2.phone_number = '0620788001'
        user2.birth_date = datetime.datetime.now().date()
        user2.save()

    def setUp(self):
        self.user, self.user2 = User.objects.all()[1:]
        self.client = APIClient()

    def test_endpoint_list(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 200)
        user_list = json.loads(response.content)

        for user in user_list:
            id = user.get('id')
            user_model = UserSerializer(model_to_dict(User.objects.get(id=id))).data
            print(user)
            print(user_model)
            self.assertEqual(user, user_model)

    def test_endpoint_create(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('user-list')
        data = {
            "password": "AzErTyUiOp#",
            "is_superuser": False,
            "username": "TestUser",
            "first_name": "test",
            "last_name": "user",
            "email": "test@user.fr",
            "is_active": True,
            "street": "11 rue de ma foucherais",
            "city": "vezin le coquet",
            "postal_code": "35132",
            "phone_number": "0620788001",
            "birth_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "groups": [],
            "user_permissions": [],
            "amis": [],
        }
        response = self.client.post(url, data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_user = User.objects.get(username='TestUser')
        self.assertTrue(test_user)

    def test_enpoint_delete(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('user-list')
        data = {
            "password": "AzErTyUiOp#",
            "is_superuser": False,
            "username": "TestUser",
            "first_name": "test",
            "last_name": "user",
            "email": "test@user.fr",
            "is_active": True,
            "street": "11 rue de ma foucherais",
            "city": "vezin le coquet",
            "postal_code": "35132",
            "phone_number": "0620788001",
            "birth_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "groups": [],
            "user_permissions": [],
            "amis": [],
        }
        response = self.client.post(url, data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_user = User.objects.get(username='TestUser')
        self.assertTrue(test_user)

        url = reverse('user-detail', args=[test_user.id])
        response = self.client.delete(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 204)

        url = reverse('user-retrieve-full', args=[test_user.id])
        response = self.client.post(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 404)

    def test_endpoint_retrieve_full(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('user-retrieve-full', args=[self.user.id])
        response = self.client.post(url, format='json')
        user = model_to_dict(self.user)
        retrieved_user = response.data
        user = UserDetailSerializer(user).data
        print(retrieved_user)
        print(user)
        # print(user.get('date_joined').strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        # print(response.data.get('date_joined'))
        # user['date_joined'] = user.get('date_joined').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        # user['birth_date'] = user.get('birth_date').strftime('%Y-%m-%d')
        self.assertEqual(user, retrieved_user)
