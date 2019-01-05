from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import survivor.models as model
from .models import Survivor


class SurvivorTests(APITestCase):

    def test_create_survivor(self):
        """
        Ensure we can create a new account object.
        """
        url = "http://127.0.0.1:8000/survivor/"
        data = {'name': 'Ana', 'age': 19, 'gender': 'F', 'last_location_longitude': "172º23'23''E'",
                'last_location_latitude': "80º21'25''N", 'infected': False, 'water': 4,
                'food': 5, 'medication': 0, "ammunition": 1, 'reports': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(model.Survivor.objects.count(), 1)
        self.assertEqual(model.Survivor.objects.get().name, 'Ana')

    def test_create_survivor2(self):
        url = "http://127.0.0.1:8000/survivor/"
        data = {'name': 'Ana', 'age': 19, 'gender': 'F', 'last_location_longitude': "172º23'23''E'",
                'last_location_latitude': "80º21'25''N", 'infected': False, 'water': 4,
                'food': 5, 'medication': 0, "ammunition": 1, 'reports': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {'name': 'Lucas', 'age': 19, 'gender': 'M', 'last_location_longitude': "60º0'0''E'",
                'last_location_latitude': "80º21'25''S", 'infected': False, 'water': 2,
                'food': 1, 'medication': 1, "ammunition": 1, 'reports': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(model.Survivor.objects.count(), 2)

    def test_creat_survivor_error(self):
        '''
        Missing one attribute, makes request error
        '''
        url = "http://127.0.0.1:8000/survivor/"
        data = {'name': 'Ana', 'age': 19, 'gender': 'F', 'last_location_longitude': "172º23'23''E'",
                'last_location_latitude': "80º21'25''N", 'infected': False, 'water': 4,
                'food': 5, 'medication': 0, 'reports': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_survivor_flag_as_infected(self):
        #import ipdb;ipdb.set_trace()
        url = "http://127.0.0.1:8000/survivor/"
        data = {'name':'Ana', 'age':19, 'gender':'F', 'last_location_longitude':"172º23'23''E'",
                    'last_location_latitude':"80º21'25''N", 'infected':False, 'water': 4,  'food':5,
                    'medication':1, 'ammunition':1, 'reports':0}
        response = self.client.post(url, data, format='json')
        data = {'name':'Paula', 'age':19, 'gender':'F', 'last_location_longitude':"172º23'23''E'",
                    'last_location_latitude':"80º21'25''N", 'infected':False, 'water': 4,  'food':5,
                    'medication':1, 'ammunition':1, 'reports':0}
        response = self.client.post(url, data, format='json')
        data = {'name':'João', 'age':19, 'gender':'M', 'last_location_longitude':"172º23'23''E'",
                    'last_location_latitude':"80º21'25''N", 'infected':False, 'water': 4,  'food':5,
                    'medication':1, 'ammunition':1, 'reports':0}
        response = self.client.post(url, data, format='json')
        data = {'name':'Lucas', 'age':19, 'gender':'M', 'last_location_longitude':"172º23'23''E'",
                    'last_location_latitude':"80º21'25''N", 'infected':False, 'water': 4,  'food':5,
                    'medication':1, 'ammunition':1, 'reports':0}
        response = self.client.post(url, data, format='json')
        url = "http://127.0.0.1:8000/infected/4"
        data = {'report': 1, 'report': 1, 'report': 1}
        response = self.client.patch(url, data, format='json')
        survivor = Survivor.objects.get(id=4)
        self.assertEqual(survivor.reports, 3)
        self.assertEqual(survivor.infected, True)
