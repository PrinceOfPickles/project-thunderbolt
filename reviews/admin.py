from django.contrib import admin
from .models import EnergyDrink, Review, DrinkType, DrinkContainer

# Register your models here.
admin.site.register(EnergyDrink)
admin.site.register(DrinkType)
admin.site.register(DrinkContainer)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'drink', 'sweetness_rating', 'sourness_rating', 'flavor_strength_rating','overall_rating', 'is_hidden')
    list_filter = ('is_hidden',)
    actions = ['hide_reviews', 'unhide_reviews']

    def hide_reviews(self, request, queryset):
        queryset.update(is_hidden=True)
    hide_reviews.short_description = "Hide selected reviews"

    def unhide_reviews(self, request, queryset):
        queryset.update(is_hidden=False)
    unhide_reviews.short_description = "Unhide selected reviews"
