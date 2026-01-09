from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()

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
    description = models.TextField(blank=True)
    taste_profile = models.TextField(blank=True)
    image = models.ImageField(upload_to='energy_drinks/')

    def __str__(self):
        return f"{self.brand} {self.series} {self.name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    drink = models.ForeignKey('EnergyDrink', on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField(blank=True, null=True)
    sweetness_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], null=True, blank=True
    )
    sourness_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], null=True, blank=True
    )
    flavor_strength_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], null=True, blank=True
    )
    overall_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], null=True, blank=True
    )
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"Review of {self.drink.brand} {self.drink.series} {self.drink.name} by {self.user.username}"
