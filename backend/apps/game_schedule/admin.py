from django.contrib import admin

from . import models

admin.site.register(models.Game)
admin.site.register(models.GameSchedule)
admin.site.register(models.Season)
