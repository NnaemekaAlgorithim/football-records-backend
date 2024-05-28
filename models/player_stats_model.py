#!/usr/bin/python3
"""Defines the PlayerStats class."""
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class PlayerStats(BaseModel, Base):
    """Represents player statistics for a MySQL database.
    
    Attributes:
        __tablename__ (str): The name of the MySQL table to store player statistics.
        stat_id (sqlalchemy String): The statistics ID (primary key).
        player_id (sqlalchemy String): The ID of the player (foreign key).
        current_team (sqlalchemy String): The name of current team.
        previous_team (sqlalchemy String): The name of the player's previous team
        joined_team_at (sqlalchemy String): When the player joined the team.
        left_team_at (sqlalchemy String): When the player left the team.
        season_played (sqlalchemy String): The season the statistics were recorded.
        match_half_played (sqlalchemy String): The match half played.
        start_match (sqlalchemy Boolean): Whether the player started the match.
        sub_in_at (sqlalchemy String): The time the player was substituted in.
        sub_out_at (sqlalchemy String): The time the player was substituted out.
        opposing_team (sqlalchemy String): The opposing team.
        match_type (sqlalchemy String): The type of match.
        control_success (sqlalchemy Integer): Number of successful controls.
        control_fail (sqlalchemy Integer): Number of failed controls.
        short_pass_success (sqlalchemy Integer): Number of successful short passes.
        short_pass_fail (sqlalchemy Integer): Number of failed short passes.
        duel_success (sqlalchemy Integer): Number of successful duels.
        duel_fail (sqlalchemy Integer): Number of failed duels.
        long_pass_success (sqlalchemy Integer): Number of successful long passes.
        long_pass_fail (sqlalchemy Integer): Number of failed long passes.
        dribble_success (sqlalchemy Integer): Number of successful dribbles.
        dribble_fail (sqlalchemy Integer): Number of failed dribbles.
        cross_success (sqlalchemy Integer): Number of successful crosses.
        cross_fail (sqlalchemy Integer): Number of failed crosses.
        shoot_success (sqlalchemy Integer): Number of successful shots.
        shoot_fail (sqlalchemy Integer): Number of failed shots.
        interception_success (sqlalchemy Integer): Number of successful interceptions.
        interception_fail (sqlalchemy Integer): Number of failed interceptions.
        one_touch_pass_success (sqlalchemy Integer): Number of successful one-touch passes.
        one_touch_pass_fail (sqlalchemy Integer): Number of failed one-touch passes.
        call_of_ball_success (sqlalchemy Integer): Number of successful calls of the ball.
        call_of_ball_fail (sqlalchemy Integer): Number of failed calls of the ball.
        tackle_success (sqlalchemy Integer): Number of successful tackles.
        tackle_fail (sqlalchemy Integer): Number of failed tackles.
        clearance_success (sqlalchemy Integer): Number of successful clearances.
        clearance_fail (sqlalchemy Integer): Number of failed clearances.
        fouled_on (sqlalchemy Integer): Number of times fouled on.
        foul_commited (sqlalchemy Integer): Number of fouls committed.
        corner_success (sqlalchemy Integer): Number of successful corners.
        corner_fail (sqlalchemy Integer): Number of failed corners.
        free_kick_success (sqlalchemy Integer): Number of successful free kicks.
        free_kick_fail (sqlalchemy Integer): Number of failed free kicks.
        penalty_kick_success (sqlalchemy Integer): Number of successful penalty kicks.
        penalty_kick_fail (sqlalchemy Integer): Number of failed penalty kicks.
        yellow_card (sqlalchemy Integer): Number of yellow cards received.
        red_card (sqlalchemy Integer): Number of red cards received.
        goal_save (sqlalchemy Integer): Number of goals saved.
        goal_conceded (sqlalchemy Integer): Number of goals conceded.
        penalty_save (sqlalchemy Integer): Number of penalties saved.
        penalty_conceded (sqlalchemy Integer): Number of penalties conceded.
        offside (sqlalchemy Integer): Number of offsides.
        goal_scored (sqlalchemy Integer): Number of goals scored.
        assists (sqlalchemy Integer): Number of assists.
        throw_in_success (sqlalchemy Integer): Number of successful throw-ins.
        throw_in_fail (sqlalchemy Integer): Number of failed throw-ins.
        created_by (sqlalchemy String): User who created the data.
        updated_by (sqlalchemy String): User who updated the data.
    """
    __tablename__ = 'player_stats'
    
    stat_id = Column(String(60), primary_key=True)
    player_id = Column(String(60), ForeignKey('players.player_id'), nullable=False)
    current_team = Column(String(128), nullable=False)
    previous_team = Column(String(128), nullable=True)
    joined_team_at = Column(String(128), nullable=True)
    left_team_at = Column(String(128), nullable=True)
    season_played = Column(String(128), nullable=True)
    match_half_played = Column(String(128), nullable=True)
    start_match = Column(Boolean, nullable=False, default=False)
    sub_in_at = Column(String(128), nullable=True)
    sub_out_at = Column(String(128), nullable=True)
    opposing_team = Column(String(128), nullable=False)
    match_type = Column(String(128), nullable=False)
    control_success = Column(Integer, nullable=True, default=0)
    control_fail = Column(Integer, nullable=True, default=0)
    short_pass_success = Column(Integer, nullable=True, default=0)
    short_pass_fail = Column(Integer, nullable=True, default=0)
    duel_success = Column(Integer, nullable=True, default=0)
    duel_fail = Column(Integer, nullable=True, default=0)
    long_pass_success = Column(Integer, nullable=True, default=0)
    long_pass_fail = Column(Integer, nullable=True, default=0)
    dribble_success = Column(Integer, nullable=True, default=0)
    dribble_fail = Column(Integer, nullable=True, default=0)
    cross_success = Column(Integer, nullable=True, default=0)
    cross_fail = Column(Integer, nullable=True, default=0)
    shoot_success = Column(Integer, nullable=True, default=0)
    shoot_fail = Column(Integer, nullable=True, default=0)
    interception_success = Column(Integer, nullable=True, default=0)
    interception_fail = Column(Integer, nullable=True, default=0)
    one_touch_pass_success = Column(Integer, nullable=True, default=0)
    one_touch_pass_fail = Column(Integer, nullable=True, default=0)
    call_of_ball_success = Column(Integer, nullable=True, default=0)
    call_of_ball_fail = Column(Integer, nullable=True, default=0)
    tackle_success = Column(Integer, nullable=True, default=0)
    tackle_fail = Column(Integer, nullable=True, default=0)
    clearance_success = Column(Integer, nullable=True, default=0)
    clearance_fail = Column(Integer, nullable=True, default=0)
    fouled_on = Column(Integer, nullable=True, default=0)
    foul_commited = Column(Integer, nullable=True, default=0)
    corner_success = Column(Integer, nullable=True, default=0)
    corner_fail = Column(Integer, nullable=True, default=0)
    free_kick_success = Column(Integer, nullable=True, default=0)
    free_kick_fail = Column(Integer, nullable=True, default=0)
    penalty_kick_success = Column(Integer, nullable=True, default=0)
    penalty_kick_fail = Column(Integer, nullable=True, default=0)
    yellow_card = Column(Integer, nullable=True, default=0)
    red_card = Column(Integer, nullable=True, default=0)
    goal_save = Column(Integer, nullable=True, default=0)
    goal_conceded = Column(Integer, nullable=True, default=0)
    penalty_save = Column(Integer, nullable=True, default=0)
    penalty_conceded = Column(Integer, nullable=True, default=0)
    offside = Column(Integer, nullable=True, default=0)
    goal_scored = Column(Integer, nullable=True, default=0)
    assists = Column(Integer, nullable=True, default=0)
    throw_in_success = Column(Integer, nullable=True, default=0)
    throw_in_fail = Column(Integer, nullable=True, default=0)
    created_by = Column(String(128), nullable=True)
    updated_by = Column(String(128), nullable=True)


    # Define relationships
    player = relationship("Player", back_populates="player_stats")

    def __init__(self, *args, **kwargs):
        """Initialize a new PlayerStats."""
        super().__init__(*args, **kwargs)
        self.stat_id = uuid4().hex
