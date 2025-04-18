from django.db import models
from django.contrib.auth.models import AbstractUser
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

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/<username>/<filename>
    return f'profile_images/{instance.username}/{filename}'


class CustomUser(AbstractUser):
    # includes username, password, email, and more
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
