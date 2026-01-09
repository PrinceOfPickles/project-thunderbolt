from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drinks/', views.drinks, name='drinks'),
    path('drinks/<int:drink_id>/', views.drink_detail, name='drink_detail'),
    path('reviews/', views.reviews, name='reviews'),
    #path('tierlists/', views.tierlists, name='tierlists'),
]