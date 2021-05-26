from django.db import models

# Create your models here.


class ParkingModel(models.Model):
    name = models.CharField(max_length=255)
    fill_priority = models.IntegerField()

class SpaceType(models.TextChoices):

    # aceita dois campos, o primeiro é como vai ser salvo no banco de dados, e o segundo é como ficará 
    # visível para o usuário
    
    CAR = 'car', 'car'
    MOTORCYCLE = 'motorcycle', 'motorcycle'

# choices será passada para o variety

class SpaceModel(models.Model):
    variety = models.CharField(max_length=255, choices=SpaceType.choices)
    level = models.ForeignKey(ParkingModel, on_delete=models.CASCADE)