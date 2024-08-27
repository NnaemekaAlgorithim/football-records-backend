from django.contrib import admin
from .models import PlayerStats, Team, TeamStats, CustomUser
from .models.player_model import Player
from .models.league_model import League
from .models.season_model import Season
from .models.match_model import Match

# Register your models here.
admin.site.register(PlayerStats)
admin.site.register(Team)
admin.site.register(TeamStats)
admin.site.register(CustomUser)
admin.site.register(Player)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(Match)