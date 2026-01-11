from django import forms
from .models import TierList

class TierListForm(forms.ModelForm):
    class Meta:
        model = TierList
        fields = ['title', 'description']