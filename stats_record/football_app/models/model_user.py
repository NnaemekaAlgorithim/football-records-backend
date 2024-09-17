import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from .base_model import BaseModel

class CustomUser(AbstractUser, BaseModel):
    """Represents a user for a MySQL database.

    Attributes:
        date_of_birth (DateField): The player's date of birth.
        is_player (BooleanField): Check if the user is a player.
        user_height (IntegerField): The user's height in centimeters.
        User_primary_position (CharField): The user's primary position.
        subscribed (BooleanField): Indicates if a user is subscribed.
        user_team (ForeignKey): The ID of the team the user belongs to.
        user_image (FileField): The user's profile image should be a professional headshot.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField(null=True, blank=True)  # Replaces user_age
    user_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def calculate_age(self):
        """Calculate and return the user's age based on date_of_birth."""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
