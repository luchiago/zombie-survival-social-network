from django.db import models
'''
In survivor\models.py we describe
the survivor and his atributs
'''
class Survivor(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    GENDERS = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    last_location_longitude = models.CharField(max_length=20, help_text="0 to 180 W/E e.g 172º 23' 23'' E")
    #e.g 172º23'23''E
    last_location_latitude = models.CharField(max_length=20, help_text="0 to 90 N/S e.g 80º 21' 25'' N")
    #e.g 80º21'25''N

    #Default is false because is supposed which the survivor is not infected
    infected = models.BooleanField(default=False)

    #His invetory is described here
    water = models.IntegerField() #4 points
    food = models.IntegerField() #3 points
    medication = models.IntegerField() #2 points
    ammunition = models.IntegerField() #1 points

    #This variable is for anothers survivors reports of contamination
    #If gets == 3, mark survivor as infected
    reports = models.IntegerField(default=0)

    def __str__(self):
        return self.name
