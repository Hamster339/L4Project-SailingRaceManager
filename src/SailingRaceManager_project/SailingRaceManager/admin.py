from django.contrib import admin
from SailingRaceManager.models import Series, Race, Sailor, Boat, RaceEntry

class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(Series,SeriesAdmin)
admin.site.register(Race)
admin.site.register(Sailor)
admin.site.register(Boat)
admin.site.register(RaceEntry)
