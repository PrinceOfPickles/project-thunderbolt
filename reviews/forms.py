from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'sweetness_rating', 'sourness_rating', 'flavor_strength_rating', 'overall_rating']