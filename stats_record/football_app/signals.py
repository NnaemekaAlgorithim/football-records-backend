from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import TeamStats
from football_app import models

@receiver(post_save, sender=TeamStats)
def populate_players(sender, instance, **kwargs):
    # Clear existing players
    instance.players.clear()

    # Get all users in the team
    team_players = settings.AUTH_USER_MODEL.objects.filter(user_team=instance.team_name)

    # Add each player to the instance's players field
    for player in team_players:
        instance.players.add(player)

@receiver(post_save, sender=TeamStats)
def update_team_stats(sender, instance, **kwargs):
    team_stats = TeamStats.objects.filter(season=instance.season, team_name=instance.team_name)

    total_goals = team_stats.aggregate(models.Sum('match_goals'))['match_goals__sum'] or 0
    total_wins = team_stats.filter(match_outcome=TeamStats.WIN).count()
    total_loses = team_stats.filter(match_outcome=TeamStats.LOSS).count()
    total_draws = team_stats.filter(match_outcome=TeamStats.DRAW).count()
    total_matches_played = team_stats.count()

    # Assuming you have a PlayerStats model with a one_touch_pass_success field
    from .models import PlayerStats
    total_passes = PlayerStats.objects.filter(
        user__user_team=instance.team_name, season=instance.season
    ).aggregate(models.Sum('one_touch_pass_success'))['one_touch_pass_success__sum'] or 0

    team_stats.update(
        total_number_of_goals=total_goals,
        total_number_of_wins=total_wins,
        total_number_of_loses=total_loses,
        total_number_of_draws=total_draws,
        total_number_of_matches_played=total_matches_played,
        total_number_of_passes=total_passes,
    )
