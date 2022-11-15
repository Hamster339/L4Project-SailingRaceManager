from django.db import models


class Series(models.Model):
    name = models.CharField(max_length=50)
    ongoing = models.BooleanField()

    def __str__(self):
        return self.name


class Race(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    completed = models.BooleanField()

    def __str__(self):
        return self.name


class Sailor(models.Model):
    name = models.CharField(max_length=50)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return self.name, self.series


class Handicap(models.Model):
    boat = models.CharField(max_length=50, primary_key=True)
    handicap = models.IntegerField()

    def __str__(self):
        return self.boat


class RaceEntry(models.Model):
    sailor_id = models.ForeignKey(Sailor, on_delete=models.CASCADE, related_name='sailor_id_set')
    race_id = models.ForeignKey(Sailor, on_delete=models.CASCADE, related_name='race_id_set')
    boat = models.ForeignKey(Handicap, on_delete=models.SET_NULL, null=True)
    race_handicap = models.IntegerField(null=True)
    time = models.DurationField(null=True)
    # default = false as on creation these will always be false
    shore_officer = models.BooleanField(default=False)
    did_not_finnish = models.BooleanField(default=False)
    score = models.IntegerField()

    def __str__(self):
        return self.sailor_id, self.race_id


    class Meta:
        # constraint represents composite primary key of sailor_id and race_id fields
        constraints = [
            models.UniqueConstraint(fields=['sailor_id', 'race_id'], name='unique_entry')
        ]