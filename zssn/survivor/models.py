from django.db import models

class Survivor(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    GENDERS = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    
    last_location_longitude = models.CharField(max_length=20)
    #0 to 180 W/E e.g 172º 23' 23'' E
    last_location_latitude = models.CharField(max_length=20)
    #0 to 90 N/S e.g 80º 21' 25'' N"

    infected = models.BooleanField(default=False)

    water = models.IntegerField()
    food = models.IntegerField()
    medication = models.IntegerField()
    ammunition = models.IntegerField()

    reports = models.IntegerField(default=0)

    def __str__(self):
        return self.name
