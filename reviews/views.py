from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import Avg
from .models import Review, EnergyDrink
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ReviewForm


def index(request):
    return render(request, 'index.html')

def drinks(request):
    drinks = EnergyDrink.objects.all().annotate(
        avg_rating=Avg('review__overall_rating', filter=models.Q(review__is_hidden=False))
    )
    return render(request, 'drinks/drinks.html', {'drinks': drinks})

def drink_detail(request, drink_id):
    drink = get_object_or_404(EnergyDrink, id=drink_id)
    reviews = Review.objects.filter(drink=drink, is_hidden=False).order_by('-created_dt')
    avg_rating = reviews.aggregate(Avg('overall_rating'))['overall_rating__avg']
    return render(request, 'drinks/drink_detail.html', {'drink': drink, 'reviews': reviews, 'avg_rating': avg_rating})

def drink_reviews(request, drink_id):
    drink = get_object_or_404(EnergyDrink, id=drink_id)
    
    return render(request, 'reviews/drink_reviews.html', {'drink': drink, 'reviews': reviews})

def reviews(request):
    reviews = Review.objects.filter(is_hidden=False)
    return render(request, 'reviews/reviews.html', {'reviews': reviews})


@login_required
def create_review(request, drink_id):
    drink = get_object_or_404(EnergyDrink, id=drink_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.drink = drink
            review.save()
            return redirect('drink_detail', drink_id=drink.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form, 'drink': drink})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('drink_detail', drink_id=review.drink.id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('drink_detail', drink_id=review.drink.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('drink_detail', drink_id=review.drink.id)
    if request.method == 'POST':
        review.delete()
        return redirect('drink_detail', drink_id=review.drink.id)
    return render(request, 'reviews/delete_review.html', {'review': review})

def faq(request):
    return render(request, 'faq.html')