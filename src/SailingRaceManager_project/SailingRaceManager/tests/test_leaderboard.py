from django.test import TestCase
from django.test import Client
import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SailingRaceManager_project.settings')
django.setup()
from SailingRaceManager.models import *


class Test_leaderboard(TestCase):

    c = None

    def setUp(self):
        self.c = Client()

    def test_current_series_number(self):
        add_series("series1", True)
        add_series("series2", True)
        add_series("series3", False)
        add_series("series4", False)
        add_series("series5", False)

        response = self.c.get('/')
        TestCase.assertEqual(self, 2, len(response.context["leaderboards"]))

    def test_past_series_number(self):
        add_series("series1", True)
        add_series("series2", True)
        add_series("series3", False)
        add_series("series4", False)
        add_series("series5", False)

        response = self.c.get('/')
        TestCase.assertEqual(self, 3, len(response.context["old_series"]))

    def test_current_series_only_completed_races_counted(self):
        s = add_series("series1", True)
        r1 = add_race(datetime.date(2021, 6, 20), "race1", s, True)
        r2 = add_race(datetime.date(2021, 6, 20), "race2", s, False)
        sa = add_sailor("sailor", s)
        b = add_boat("topper", 500)
        re1 = add_race_entry(sa, r1, b, 500, datetime.timedelta(minutes=31, seconds=42), False, False, 1)
        re2 = add_race_entry(sa, r2, b, 500, datetime.timedelta(minutes=31, seconds=42), False, False, 2)

        response = self.c.get('/')
        TestCase.assertEqual(self, 1, response.context["leaderboards"][0]["leaderboard"][0]["score"])

    def test_current_series_order(self):
        s = add_series("series1", True)
        sa1 = add_sailor("sailor1", s)
        sa2 = add_sailor("sailor2", s)
        b = add_boat("topper", 500)

        r1 = add_race(datetime.date(2021, 6, 20), "race1", s, True)
        r2 = add_race(datetime.date(2021, 7, 20), "race2", s, True)

        re1 = add_race_entry(sa1, r1, b, 500, datetime.timedelta(minutes=31, seconds=42), False, False, 10)
        re2 = add_race_entry(sa1, r2, b, 500, datetime.timedelta(minutes=31, seconds=42), False, False, 5)
        re3 = add_race_entry(sa2, r1, b, 500, datetime.timedelta(minutes=31, seconds=42), False, False, 1)
        re4 = add_race_entry(sa2, r2, b, 500, datetime.timedelta(minutes=31, seconds=42), False, False, 1)

        response = self.c.get('/')
        TestCase.assertEqual(self, "sailor2", response.context["leaderboards"][0]["leaderboard"][0]["name"])
        TestCase.assertEqual(self, "sailor1", response.context["leaderboards"][0]["leaderboard"][1]["name"])

# helper functions to add things to the database
def add_series(name, ongoing):
    p = Series.objects.get_or_create(name=name, ongoing=ongoing)[0]
    p.save()
    return p


def add_race(date, name, series_id, completed):
    p = Race.objects.get_or_create(date=date, name=name, series_id=series_id, completed=completed)[0]
    p.save()
    return p


def add_sailor(name, series_id):
    p = Sailor.objects.get_or_create(name=name, series_id=series_id)[0]
    p.save()
    return p


def add_boat(boat, num):
    p = Boat.objects.get_or_create(boat=boat, handicap=num)[0]
    return p


def add_race_entry(sailor_id, race_id, boat, race_handicap, time, shore_officer, did_not_finnish, score):
    p = RaceEntry.objects.get_or_create(sailor_id=sailor_id, race_id=race_id, boat=boat, race_handicap=race_handicap,
                                        time=time, shore_officer=shore_officer, did_not_finnish=did_not_finnish,
                                        score=score)[0]
    p.save()
    return p