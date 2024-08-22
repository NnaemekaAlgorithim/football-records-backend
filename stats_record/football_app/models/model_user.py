import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_age = models.IntegerField(null=True, blank=True)
    user_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
