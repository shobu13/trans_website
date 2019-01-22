import json

from django.forms import model_to_dict

import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.contrib.auth.models import User

from vie_quotidienne.models import SalleDeFete
from vie_quotidienne.serializers import SalleDeFeteSerializer, SalleDeFeteDetailSerializer


class SalleDeFeteViewsetTest(APITestCase):
    """
    class de test des endpoints lié aux users.
    """

    @classmethod  # <- setUpClass doit être une méthode de classe, attention !
    def setUpTestData(cls):
        User.objects.create_superuser(username='admin', password='sysadmin', email='').save()
        user = User.objects.create_user('Shobu', 'shobu13@hotmail.fr', 'AzErTy#')
        SalleDeFete.objects.create(nom="test", description="meh", adresse="meh", )

    def setUp(self):
        self.root, self.user2 = User.objects.all()[0:]
        self.client = APIClient()

        self.viewset_name = 'salle-de-fete'
        self.serializer = SalleDeFeteSerializer
        self.detail_serializer = SalleDeFeteDetailSerializer
        self.test_object = SalleDeFete
        self.data = {
            "nom": "test2",
            "adresse": "meh",
            "description": "blu"
        }

    def test_endpoint_list(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse(self.viewset_name + '-list')
        response = self.client.get(url, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 200)
        object_list = json.loads(response.content)
        for object_data in object_list:
            id = object_data.get('id')
            object_model = self.serializer(model_to_dict(self.test_object.objects.get(id=id))).data
            print(object_model)
            print(object_model)
            self.assertEqual(object_model, object_data)

        self.client.logout()
        response = self.client.get(url, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 401)

    def test_endpoint_create(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse(self.viewset_name + '-list')
        response = self.client.post(url, data=self.data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        object_model = self.test_object.objects.all()[1]
        self.assertTrue(object_model)

        self.client.logout()
        response = self.client.get(url, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 401)

    def test_enpoint_delete(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse(self.viewset_name + '-list')
        response = self.client.post(url, data=self.data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        object_model = self.test_object.objects.all()[1]
        self.assertTrue(object_model)

        self.client.logout()

        url = reverse(self.viewset_name + '-detail', args=[object_model.id])
        response = self.client.delete(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 401)

        self.assertTrue(self.client.login(username='admin', password='sysadmin'))

        url = reverse(self.viewset_name + '-detail', args=[object_model.id])
        response = self.client.delete(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 204)

        url = reverse(self.viewset_name + '-detail', args=[object_model.id])
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 404)

    def test_endpoint_retrieve(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse(self.viewset_name + '-detail', args=[1])
        response = self.client.get(url, format='json')
        object_model = self.test_object.objects.first()
        retrieved_object = response.data
        object_data = self.detail_serializer(object_model).data
        print(retrieved_object)
        print(object_data)
        # print(user.get('date_joined').strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        # print(response.data.get('date_joined'))
        # user['date_joined'] = user.get('date_joined').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        # user['birth_date'] = user.get('birth_date').strftime('%Y-%m-%d')
        self.assertEqual(object_data, retrieved_object)
