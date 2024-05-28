#!/usr/bin/python3
"""Defines the Team class."""
from uuid import uuid4
from sqlalchemy import Column, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base_model import Base

class Team(BaseModel, Base):
    """Represents a team for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table team.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store teams.
        team_id (sqlalchemy String): The team's ID.
        team_name (sqlalchemy String): The team's name.
        team_logo (sqlalchemy Text): The team's logo path.
        created_by (sqlalchemy String): User who created the team.
        updated_by (sqlalchemy String): User who last updated the team.
    """
    __tablename__ = "team"
    team_id = Column(String(60), primary_key=True)
    team_name = Column(String(128), nullable=False, unique=True)  # Unique constraint on team_name
    team_logo = Column(Text, nullable=True)  # Assuming logo is stored as a path to the image file
    created_by = Column(String(128), nullable=True)
    updated_by = Column(String(128), nullable=True)

    players = relationship("Player", back_populates="team")

    def __init__(self, *args, **kwargs):
        """Initialize a new Team."""
        super().__init__(*args, **kwargs)
        self.team_id = uuid4().hex
