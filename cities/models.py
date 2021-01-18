from django.db import models

class City(models.Model):
    name = models.TextField()
    distances = models.TextField()
