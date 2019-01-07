from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Survivor


class SurvivorTests(APITestCase):

    def test_create_survivor(self):

        url = "http://127.0.0.1:8000/survivor/"
        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        self.client.post(url, data, format='json')
        survivor = Survivor.objects.get(id=1)
        self.assertEqual(survivor.name, "Ana")
        self.assertEqual(survivor.age, 19)
        self.assertEqual(survivor.gender, "F")
        self.assertEqual(survivor.last_location_longitude, "172º23'23''E'")
        self.assertEqual(survivor.last_location_latitude, "80º21'25''N")
        self.assertEqual(survivor.water, 4)
        self.assertEqual(survivor.food, 5)
        self.assertEqual(survivor.medication, 0)
        self.assertEqual(survivor.ammunition, 1)
        self.assertEqual(survivor.infected, False)
        self.assertEqual(survivor.reports, 0)

    def test_create_multiple_survivors(self):

        url = "http://127.0.0.1:8000/survivor/"
        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        self.client.post(url, data, format='json')
        data = {"name": "Lucas", "age": 20, "gender": "M", "last_location_longitude": "60º0'0''E'",
                "last_location_latitude": "80º21'25''S", "water": 2,
                "food": 1, "medication": 1, "ammunition": 1}
        self.client.post(url, data, format='json')
        data = {"name": "Gabriel", "age": 21, "gender": "O", "last_location_longitude": "60º1'12''E'",
                "last_location_latitude": "80º12'25''S", "water": 5,
                "food": 0, "medication": 0, "ammunition": 0}
        self.client.post(url, data, format='json')

        self.assertEqual(Survivor.objects.count(), 3)
        survivor = Survivor.objects.get(id=2)
        self.assertEqual(survivor.name, "Lucas")
        self.assertEqual(survivor.water, 2)

    def test_get_survivor_detail(self):

        url = "http://127.0.0.1:8000/survivor/"
        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        self.client.post(url, data, format='json')

        url = "http://127.0.0.1:8000/survivor/1/"
        response = self.client.get(url, data, format='json')
        self.assertIn('"name":"Ana"', response.content.decode())
        self.assertIn('"age":19', response.content.decode())
        self.assertIn('"gender":"F"', response.content.decode())
        self.assertIn('"water":4', response.content.decode())
        self.assertIn('"food":5', response.content.decode())
        self.assertIn('"medication":0', response.content.decode())
        self.assertIn('"ammunition":1', response.content.decode())


    def test_survivor_reports(self):

        url = "http://127.0.0.1:8000/survivor/"
        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        response = self.client.post(url, data, format='json')

        url = "http://127.0.0.1:8000/reports/"
        response = self.client.get(url, data, format='json')
        self.assertIn('"Percentage of infected survivors":"0.0%"', response.content.decode())
        self.assertIn('"Percentage of non-infected survivors":"100.0%"', response.content.decode())
        self.assertIn('"Average amount of water by survivor":4.0', response.content.decode())
        self.assertIn('"Average amount of food by survivor":5.0', response.content.decode())
        self.assertIn('"Average amount of medication by survivor":0.0', response.content.decode())
        self.assertIn('"Average amount of ammunition by survivor":1.0', response.content.decode())
        self.assertIn('"Points lost because of infected survivor":0', response.content.decode())

    def test_survivor_update_location(self):

        url = "http://127.0.0.1:8000/survivor/"
        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        self.client.post(url, data, format='json')

        url = "http://127.0.0.1:8000/updatelocation/1/"
        data = {"last_location_longitude":"150º23'23''E'", "last_location_latitude":"50º21'25''N"}
        self.client.patch(url, data, format='json')

        survivor = Survivor.objects.get(id=1)
        self.assertEqual(survivor.last_location_longitude, "150º23'23''E'")
        self.assertEqual(survivor.last_location_latitude, "50º21'25''N")

    def test_survivor_flag_as_infected(self):

        url = "http://127.0.0.1:8000/survivor/"
        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        self.client.post(url, data, format='json')
        data = {"name":'Paula', "age":21, "gender":'F',"last_location_longitude":"152º23'23''E'",
                "last_location_latitude":"70º21'25''N", "water": 2,
                "food":6, "medication":3, "ammunition":2}
        self.client.post(url, data, format='json')
        data = {"name":'João', "age":30, "gender":'M',"last_location_longitude":"272º23'23''E'",
                "last_location_latitude":"20º21'25''N", "water": 1,
                "food":9, "medication":8, "ammunition":5}
        self.client.post(url, data, format='json')
        data = {"name":'Lucas', "age":15, "gender":'M',"last_location_longitude":"155º23'23''E'",
                "last_location_latitude":"90º21'25''N", "water": 5,
                "food":2, "medication":5, "ammunition":7}
        self.client.post(url, data, format='json')

        url = "http://127.0.0.1:8000/infected/1/"
        data = {'report1': '2', 'report2': '3', 'report3': '4'}
        self.client.patch(url, data, format='json')

        survivor = Survivor.objects.get(id=1)
        self.assertEqual(survivor.reports, 3)
        self.assertEqual(survivor.infected, True)

        url = "http://127.0.0.1:8000/infected/2/"
        data = {'report2': '3', 'report3': '4'}
        self.client.patch(url, data, format='json')

        survivor = Survivor.objects.get(id=2)
        self.assertEqual(survivor.reports, 2)
        self.assertEqual(survivor.infected, False)

    def test_survivor_trade(self):

        url = "http://127.0.0.1:8000/survivor/"

        data = {"name": "Ana", "age": 19, "gender": "F", "last_location_longitude": "172º23'23''E'",
                "last_location_latitude": "80º21'25''N", "water": 4,
                "food": 5, "medication": 0, "ammunition": 1}
        self.client.post(url, data, format='json')
        data = {"name":'Paula', "age":21, "gender":'F',"last_location_longitude":"152º23'23''E'",
                "last_location_latitude":"70º21'25''N", "water": 2,
                "food":6, "medication":3, "ammunition":2}
        self.client.post(url, data, format='json')
        data = {"name":'João', "age":30, "gender":'M',"last_location_longitude":"272º23'23''E'",
                "last_location_latitude":"20º21'25''N", "water": 1,
                "food":9, "medication":8, "ammunition":6}
        self.client.post(url, data, format='json')
        data = {"name":'Lucas', "age":15, "gender":'M',"last_location_longitude":"155º23'23''E'",
                "last_location_latitude":"90º21'25''N", "water": 5,
                "food":2, "medication":5, "ammunition":7}
        self.client.post(url, data, format='json')

        url = "http://127.0.0.1:8000/trade/"
        data = {"survivor1_id" : 2,"items1_trade": {"water": 1, "medication": 1},
                "survivor2_id": 3,"items2_trade": {"ammunition" : 6}}
        response = self.client.patch(url, data, format='json')

        survivor1 = Survivor.objects.get(id=2)
        survivor2 = Survivor.objects.get(id=3)
        self.assertEqual(survivor1.ammunition, 8)
        self.assertEqual(survivor1.water, 1)
        self.assertEqual(survivor1.medication, 2)
        self.assertEqual(survivor2.ammunition, 0)
        self.assertEqual(survivor2.water, 2)
        self.assertEqual(survivor2.medication, 9)
