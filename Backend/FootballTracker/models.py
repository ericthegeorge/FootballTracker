from django.db import models

# Create your models here.

# EXAMPLE HERE YOUR MOST WELCOME:

'''
class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="decks")
'''


