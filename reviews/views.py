from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import Avg
from django.views.generic import ListView
from .models import Review, EnergyDrink

def index(request):
    return render(request, 'index.html')

def drinks(request):
    drinks = EnergyDrink.objects.all().annotate(
        avg_rating=Avg('review__overall_rating', filter=models.Q(review__is_hidden=False))
    )
    return render(request, 'drinks.html', {'drinks': drinks})

def drink_detail(request, drink_id):
    drink = get_object_or_404(EnergyDrink, id=drink_id)
    return render(request, 'drink_detail.html', {'drink': drink})

def drink_reviews(request, drink_id):
    drink = get_object_or_404(EnergyDrink, id=drink_id)
    reviews = Review.objects.filter(drink=drink, is_hidden=False).order_by('-created_dt')
    return render(request, 'drink_reviews.html', {'drink': drink, 'reviews': reviews})

def reviews(request):
    reviews = Review.objects.filter(is_hidden=False)
    return render(request, 'reviews.html', {'reviews': reviews})

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(is_hidden=False)

