from django.contrib import admin
from .models import PlayerStats, Team, TeamStats, CustomUser

# Register your models here.
admin.site.register(PlayerStats)
admin.site.register(Team)
admin.site.register(TeamStats)
admin.site.register(CustomUser)