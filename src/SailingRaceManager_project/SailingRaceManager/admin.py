from django.contrib import admin
from SailingRaceManager.models import Series, Race, Sailor, Boat, RaceEntry
# Register your models here.

admin.site.register(Series)
admin.site.register(Race)
admin.site.register(Sailor)
admin.site.register(Boat)
admin.site.register(RaceEntry)
