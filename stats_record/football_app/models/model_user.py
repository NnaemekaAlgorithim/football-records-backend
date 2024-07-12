from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from .base_model import BaseModel

class CustomUser(AbstractUser, BaseModel):
    """Represents a user for a MySQL database.

    Attributes:
        user_age (IntegerField): The player's age.
        is_player (BooleanField) Check if the user is a player.
        user_height (IntegerField): The user's height in centimeters.
        User_primary_position (CharField): The user's primary position.
        subscribed (BooleanField): Indicates if a user is subscribed.
        user_team (ForeignKey): The ID of the team the user belongs to.
        user_image (File): The user's profile image.
    """
    user_age = models.IntegerField(null=True, blank=True)
    is_player = models.BooleanField(default=False)
    user_height = models.IntegerField(null=True, blank=True)
    user_primary_position = models.CharField(max_length=128, null=True, blank=True)
    subscribed = models.BooleanField(default=False)
    user_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='players', null=True, blank=True)
    user_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        if self.is_player and not self.user_team:
            raise ValidationError("Players must belong to a team.")
        if self.is_player and not self.user_height:
            raise ValidationError("Players must provide their height.")
        if self.is_player and not self.user_age:
            raise ValidationError("Players must provide their age.")

        super().save(*args, **kwargs)
