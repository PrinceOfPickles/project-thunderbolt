from django.urls import path
from . import views

urlpatterns = [
    path('', views.TierList, name='tierlists'),
    path('<int:tierlist_id>/', views.tierlist_detail, name='tierlist_detail'),
]
