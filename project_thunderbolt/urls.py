from django.contrib import admin
from django.urls import path
from reviews import views as reviews_views
from tierlists import views as tierlists_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', reviews_views.index, name='index'),
    path('drinks/', reviews_views.drinks, name='drinks'),
    path('drinks/<int:drink_id>/', reviews_views.drink_detail, name='drink_detail'),
    path('drinks/<int:drink_id>/reviews/', reviews_views.drink_reviews, name='drink_reviews'),
    path('reviews/', reviews_views.reviews, name='reviews'),
    
    path('tierlists/', tierlists_views.TierList, name='tierlists'),
    path('tierlists/<int:tierlist_id>/', tierlists_views.tierlist_detail, name='tierlist_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
