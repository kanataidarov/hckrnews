from django.db import models

class City(models.Model):
    name = models.TextField(unique=True)
    order = models.IntegerField(unique=True, default=0)
    distances = models.TextField()

class CityResponse(models.Model): 
    startCity = models.TextField()
    pathWeight = models.IntegerField()
    path = models.TextField() 

