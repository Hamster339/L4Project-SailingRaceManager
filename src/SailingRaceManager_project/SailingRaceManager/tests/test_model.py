from django.test import TestCase
import os
import django
import datetime
from SailingRaceManager.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SailingRaceManager_project.settings')
django.setup()


class TestSeries(TestCase):
    def test_series_valid(self):
        r = Series.objects.get_or_create(name="Series1", ongoing="True")
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_Series_invalid_datatype_ongoing(self):
        with self.assertRaisesMessage(django.core.exceptions.ValidationError, ""):
            r = Series.objects.create(name="Series1", ongoing="false")
            r[0].save()

    # Cannot find anything that won't be automatically turned into a string and accepted. Similar tests in other
    # places have been omited
    def test_Series_invalid_dataType_name(self):
        pass

    def test_Series_invalid_notNull_name(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Series.objects.create(name=None, ongoing=True)
            r[0].save()

    def test_Series_invalid_NotNull_ongoing(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Series.objects.create(name="Series1", ongoing=None)
            r[0].save()


class TestSailor(TestCase):
    def test_Sailor_valid(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        r = Sailor.objects.get_or_create(name="Sailor1", series_id=s)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_Sailor_invalid_datatype_SeriesID(self):
        with self.assertRaisesMessage(ValueError, ""):
            r = Sailor.objects.create(name="Series1", series_id="Series1")
            r[0].save()

    def test_Sailor_invalid_notNull_name(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
            r = Sailor.objects.create(name=None, series_id=s)
            r[0].save()

    def test_Sailor_invalid_NotNull_SeriesID(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Sailor.objects.create(name="Sailor1", series_id=None)
            r[0].save()


class TestBoat(TestCase):
    def test_Boat_valid(self):
        r = Boat.objects.get_or_create(boat="topper", handicap=500)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_Boat_invalid_datatype_handicap(self):
        with self.assertRaisesMessage(ValueError, ""):
            r = Boat.objects.get_or_create(boat="topper", handicap="hello")
            r[0].save()

    # boat is a primary key. In SQLight, primary keys can be null for some reason. The constraint must be
    # enforced in forms
    def test_Boat_invalid_notNull_boat(self):
        pass

    def test_Sailor_invalid_NotNull_SeriesID(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Boat.objects.get_or_create(boat="topper", handicap=None)
            r[0].save()

class TestRace(TestCase):
    def test_Race_valid(self):
        s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
        r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_Race_Invalid_datatype_date(self):
        with self.assertRaisesMessage(django.core.exceptions.ValidationError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date="2022", name="race1", series_id=s, completed=True)

    def test_Race_Invalid_datatype_seriesID(self):
        with self.assertRaisesMessage(ValueError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id="series1", completed=True)

    def test_Race_Invalid_datatype_completed(self):
        with self.assertRaisesMessage(django.core.exceptions.ValidationError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed="true")

    def test_Race_Invalid_notNull_date(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date=None, name="race1", series_id=s, completed=True)

    def test_Race_Invalid_notNull_name(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name=None, series_id=s, completed=True)

    def test_Race_Invalid_notNull_seriesID(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=None, completed=True)

    def test_Race_Invalid_notNull_completed(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=None)


class TestRaceEntry(TestCase):
    def test_RaceEntry_Valid(self):

    def test_RaceEntry_Invalid_Datatype_sailor_id(self):

    def test_RaceEntry_Invalid_Datatype_race_id(self):

    def test_RaceEntry_Invalid_Datatype_(self):

    def test_RaceEntry_Invalid_Datatype_(self):

    def test_RaceEntry_Invalid_Datatype_(self):

    def test_RaceEntry_Invalid_Datatype_(self):

    def test_RaceEntry_Invalid_Datatype_(self):

    def test_RaceEntry_Invalid_Datatype_(self):

    def test_RaceEntry_Invalid_NotNull_sailor_id(self):

    def test_RaceEntry_Invalid_NotNull_race_id(self):

    def test_RaceEntry_Invalid_NotNull_shore_officer(self):

    def test_RaceEntry_Invalid_NotNull_did_not_finnish(self):

    def test_RaceEntry_Invalid_Null_boat(self):

    def test_RaceEntry_Invalid_Null_race_handicap(self):

    def test_RaceEntry_Invalid_Null_time(self):

    def test_RaceEntry_Invalid_Null_score(self):
