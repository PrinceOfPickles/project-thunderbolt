from django.contrib import admin
from .models import EnergyDrink, Review, DrinkType, DrinkContainer

# Register your models here.
admin.site.register(EnergyDrink)
admin.site.register(Review)
admin.site.register(DrinkType)
admin.site.register(DrinkContainer)