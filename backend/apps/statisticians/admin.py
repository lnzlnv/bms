from django.contrib import admin

from . import models

admin.site.register(models.Stat)
admin.site.register(models.PlayerStat)
admin.site.register(models.TeamStat)
admin.site.register(models.PlayerGameStat)
admin.site.register(models.PointsClassification)
admin.site.register(models.Substitution)
admin.site.register(models.InGamePlayer)
admin.site.register(models.PointsInAQuarter)
admin.site.register(models.TeamTimeStatsAnalysis)
admin.site.register(models.TeamSeasonStat)
admin.site.register(models.OfficiateHistory)
