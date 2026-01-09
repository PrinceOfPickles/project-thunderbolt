from django.contrib import admin
from .models import TierList, TierListItem

admin.site.register(TierListItem)

@admin.register(TierList)
class TierListAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_hidden')
    list_filter = ('is_hidden',)
    actions = ['hide_tierlists', 'unhide_tierlists']

    def hide_tierlists(self, request, queryset):
        queryset.update(is_hidden=True)
    hide_tierlists.short_description = "Hide selected tier lists"

    def unhide_tierlists(self, request, queryset):
        queryset.update(is_hidden=False)
    unhide_tierlists.short_description = "Unhide selected tier lists"

