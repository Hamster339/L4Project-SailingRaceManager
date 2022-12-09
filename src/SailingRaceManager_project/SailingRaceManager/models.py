# Models file specifies database schema
from django.db import models
from django.template.defaultfilters import slugify


# class represents a series' of races
class Series(models.Model):
    name = models.CharField(max_length=50)
    ongoing = models.BooleanField()
    # slug field not in ERD as only purpose is the displaying of old series pages.
    slug = models.SlugField(unique=True)

    # override save method to save with slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Series, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class represents sailing races
class Race(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    completed = models.BooleanField()

    def __str__(self):
        return self.name


# class represents sailors. sailors are unique to each series.
class Sailor(models.Model):
    name = models.CharField(max_length=50)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return "{},{}".format(self.name, self.series_id)


# class records RYA Portsmouth Yardstick handicap number for each boat that can be used in a race
class Boat(models.Model):
    boat = models.CharField(max_length=50, primary_key=True)
    handicap = models.IntegerField()

    def __str__(self):
        return self.boat


# class represents a sailors entry in a race
class RaceEntry(models.Model):
    sailor_id = models.ForeignKey(Sailor, on_delete=models.CASCADE, related_name='sailor_id_set')
    race_id = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='race_id_set')
    boat = models.ForeignKey(Boat, on_delete=models.SET_NULL, null=True)
    race_handicap = models.IntegerField(null=True)
    time = models.DurationField(null=True)
    # default = false as on creation these will always be false
    shore_officer = models.BooleanField(default=False)
    did_not_finnish = models.BooleanField(default=False)
    score = models.IntegerField(null=True)

    def __str__(self):
        return "{},{}".format(self.sailor_id, self.race_id)

    class Meta:
        # constraint represents composite primary key of sailor_id and race_id fields
        constraints = [
            models.UniqueConstraint(fields=['sailor_id', 'race_id'], name='compensate primary key'),
        ]
