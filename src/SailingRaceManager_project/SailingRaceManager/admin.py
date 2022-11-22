from django.contrib import admin
from SailingRaceManager.models import Series, Race, Sailor, Handicap, RaceEntry
# Register your models here.

admin.site.register(Series)
admin.site.register(Race)
admin.site.register(Sailor)
admin.site.register(Handicap)
admin.site.register(RaceEntry)
