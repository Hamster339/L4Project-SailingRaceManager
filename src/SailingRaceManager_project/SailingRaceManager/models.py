# Models file specifies database schema
import datetime

from django.db import models
from django.template.defaultfilters import slugify


# class represents a series' of races
class Series(models.Model):
    name = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    SOscore = models.IntegerField(default=7)
    DNFscore = models.IntegerField(default=15)
    DNCscore = models.IntegerField(default=20)
    discountRatio = models.CharField(max_length=8, default="0:0")
    # slug field not in ERD as only purpose is the displaying of old series pages.
    slug = models.SlugField(unique=True)

    # override save method to save with slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        slug = slugify(self.name)
        existing_series = Series.objects.filter(slug=slug).exclude(pk=self.pk)
        inc = 2
        while existing_series.count() != 0:
            slug = slugify(self.name) + "-" + str(inc)
            existing_series = Race.objects.filter(slug=slug).exclude(pk=self.pk)
            inc += 1
        self.slug = slug
        super(Series, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class represents sailing races
class Race(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    completed = models.BooleanField()
    # slug field not in ERD as only purpose is the displaying of old series pages.
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # compute sulg, adding and incrimenting a number untill no race with same slug exists
        slug = slugify(self.name)
        existing_races = Race.objects.filter(slug=slug).exclude(pk=self.pk)
        inc = 2
        while existing_races.count() != 0:
            slug = slugify(self.name) + "-" + str(inc)
            existing_races = Race.objects.filter(slug=slug).exclude(pk=self.pk)
            inc += 1
        self.slug = slug

        is_new = self._state.adding is True

        super(Race, self).save(*args, **kwargs)

        # If creating and not updating, add race entries
        if is_new:
            sailors = Sailor.objects.filter(series_id=self.series_id)
            for s in sailors:
                RaceEntry.objects.get_or_create(sailor_id=s, race_id=self)

    def __str__(self):
        return self.name


# class represents sailors. sailors are unique to each series.
class Sailor(models.Model):
    name = models.CharField(max_length=50)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        is_new = self._state.adding is True

        super(Sailor, self).save(*args, **kwargs)

        # If creating and not updating, add race entries
        if is_new:
            races = Race.objects.filter(series_id=self.series_id)
            for r in races:
                RaceEntry.objects.get_or_create(sailor_id=self, race_id=r)

    def __str__(self):
        return "{},{}".format(self.name, self.series_id)


# class records RYA Portsmouth Yardstick handicap number for each boat that can be used in a race
class Boat(models.Model):
    boat = models.CharField(max_length=100)
    handicap = models.IntegerField()

    def __str__(self):
        return self.boat


# class represents a sailors entry in a race
class RaceEntry(models.Model):
    sailor_id = models.ForeignKey(Sailor, on_delete=models.CASCADE, related_name='sailor_id_set')
    race_id = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='race_id_set')
    boat = models.ForeignKey(Boat, on_delete=models.SET_NULL, null=True, default=None)
    race_handicap = models.IntegerField(null=True, default=None)
    time = models.DurationField(default=datetime.timedelta(seconds=0))
    # default = false as on creation these will always be false
    shore_officer = models.BooleanField(default=False)
    did_not_finish = models.BooleanField(default=False)
    corrected_time = models.DurationField(default=datetime.timedelta(seconds=0))

    def __str__(self):
        return "{},{}".format(self.sailor_id, self.race_id)

    # Recalculate score whenever database updated
    def save(self, *args, **kwargs):
        if (self.time != datetime.timedelta(seconds=0)) and (self.boat is not None) and (
                self.race_handicap is not None):
            c_time = (self.time.seconds * 1000) // self.race_handicap
            self.corrected_time = datetime.timedelta(seconds=c_time)
        else:
            self.corrected_time = datetime.timedelta(seconds=0)

        super(RaceEntry, self).save(*args, **kwargs)

    class Meta:
        # constraint represents composite primary key of sailor_id and race_id fields
        constraints = [
            models.UniqueConstraint(fields=['sailor_id', 'race_id'], name='compensate primary key'),
        ]
