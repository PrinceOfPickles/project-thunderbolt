from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TierList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tier_structure = models.JSONField(default=dict, blank=True)  # Lists stored in JSON
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class TierListItem(models.Model):
    tier_list = models.ForeignKey(TierList, on_delete=models.CASCADE)
    drink = models.ForeignKey('reviews.EnergyDrink', on_delete=models.CASCADE)
    tier = models.CharField(max_length=50)
    position = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.drink.name} in {self.tier_list.title}"