from django import forms
from .models import TierList
from reviews.models import EnergyDrink

class TierListForm(forms.ModelForm):
    class Meta:
        model = TierList
        fields = ['title', 'description']

class AddDrinkToTierListForm(forms.Form):
    drink = forms.ModelChoiceField(queryset=EnergyDrink.objects.all(), label="Select Drink")
    tier = forms.ChoiceField(choices=[
        ('S-Tier', 'S-Tier'),
        ('A-Tier', 'A-Tier'),
        ('B-Tier', 'B-Tier'),
        ('C-Tier', 'C-Tier'),
        ('D-Tier', 'D-Tier'),
        ('F-Tier', 'F-Tier'),
    ], label="Select Tier")