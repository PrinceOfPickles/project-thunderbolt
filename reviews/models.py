from django.db import models
from django.contrib.auth.models import User

class DrinkType(models.Model):
    type = models.CharField(max_length=50, unique=True) # Carbonated, Non-carbonated, Powdered

    def __str__(self):
        return self.type

class DrinkContainer(models.Model):
    type = models.CharField(max_length=50, unique=True) # Aluminum can, Plastic bottle, Glass bottle, Energy shot (~50ml), Micro shot (~5-25ml)

    def __str__(self):
        return self.type

class EnergyDrink(models.Model):
    brand = models.CharField(max_length=50)
    series = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    drink_type = models.ForeignKey(
        DrinkType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    drink_container = models.ForeignKey(
        DrinkContainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    taste_profile = models.TextField()
    image = models.ImageField(upload_to='energy_drinks/')

    def __str__(self):
        return f"{self.brand} {self.series} {self.name}"

class Review(models.Model):
    drink = 
