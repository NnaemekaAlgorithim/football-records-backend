#!/usr/bin/python3
"""Defines the Player class."""
from uuid import uuid4
from sqlalchemy import Boolean, Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base_model import Base

class Player(BaseModel, Base):
    """Represents a player for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table player.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store players.
        player_id (sqlalchemy String): The player's ID.
        player_first_name (sqlalchemy String): The player's first name.
        player_last_name (sqlalchemy String): The player's last name.
        player_age (sqlalchemy Integer): The player's age.
        player_team (sqlalchemy String): The ID of the team the player belongs to.
        player_image (sqlalchemy Text): The player's image path.
        player_height (sqlalchemy Integer): The player's height in centimeters.
        player_primary_position (sqlalchemy String): The player's primary position.
        subscribed (sqlalchemy boolean): Indicates if a player is subscribed.
        created_by (sqlalchemy String): User who created the player.
        updated_by (sqlalchemy String): User who last updated the player.
    """
    __tablename__ = "player"
    player_id = Column(String(60), primary_key=True)
    player_first_name = Column(String(128), nullable=False)
    player_last_name = Column(String(128), nullable=False)
    player_age = Column(Integer, nullable=False)
    player_team = Column(String(60), ForeignKey('team.team_id'), nullable=False)
    player_image = Column(Text, nullable=True)  # Assuming image is stored as a path to the image file
    player_height = Column(Integer, nullable=False)
    player_primary_position = Column(String(128), nullable=False)
    subscribed = Column(Boolean, nullable=False, default=False)
    created_by = Column(String(128), nullable=True)
    updated_by = Column(String(128), nullable=True)

    team = relationship("Team", back_populates="players")

    def __init__(self, *args, **kwargs):
        """Initialize a new Player."""
        super().__init__(*args, **kwargs)
        self.player_id = uuid4().hex
