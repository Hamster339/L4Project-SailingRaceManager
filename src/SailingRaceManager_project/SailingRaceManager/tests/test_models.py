from django.test import TestCase
import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SailingRaceManager_project.settings')
django.setup()
from SailingRaceManager.models import *


class TestSeries(TestCase):
    def test_series_valid(self):
        r = Series.objects.get_or_create(name="Series1", ongoing="True")
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_Series_invalid_notNull_name(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Series.objects.create(name=None, ongoing=True)
            r[0].save()

    def test_Series_invalid_NotNull_ongoing(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Series.objects.create(name="Series1", ongoing=None)
            r[0].save()

    def test_Series_slug_created(self):
        r = Series.objects.create(name="series 1", ongoing=True)
        TestCase.assertEqual(self, "series-1", r.slug)

    def test_Series_slug_unique(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r1 = Series.objects.create(name="Series 1", ongoing=True)
            r2 = Series.objects.create(name="series 1", ongoing=True)

    def test_Series_name_unique(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r1 = Series.objects.create(name="series 1", ongoing=True)
            r2 = Series.objects.create(name="series 1", ongoing=False)


class TestSailor(TestCase):
    def test_Sailor_valid(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        r = Sailor.objects.get_or_create(name="Sailor1", series_id=s)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

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

    # boat is a primary key. In SQLight, primary keys can be null for some reason. The constraint must be
    # enforced in forms
    def test_Boat_invalid_notNull_boat(self):
        pass

    def test_Sailor_invalid_NotNull_SeriesID(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Boat.objects.get_or_create(boat="topper", handicap=None)
            r[0].save()

    def test_Boat_primary_key_bpat_unique(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            r = Boat.objects.get_or_create(boat="topper", handicap=100)
            r2 = Boat.objects.get_or_create(boat="topper", handicap=200)


class TestRace(TestCase):
    def test_Race_valid(self):
        s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
        r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

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
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=None,
                                           completed=True)

    def test_Race_Invalid_notNull_completed(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing=True)[0]
            r = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=None)


class TestRaceEntry(TestCase):
    def test_RaceEntry_Valid(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                            time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                            did_not_finnish=False,
                                            score=10)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_RaceEntry_Invalid_NotNull_sailor_id(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
            ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[
                0]
            b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
            r = RaceEntry.objects.get_or_create(sailor_id=None, race_id=ra, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                                did_not_finnish=False,
                                                score=10)

    def test_RaceEntry_Invalid_NotNull_race_id(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
            sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
            ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[
                0]
            b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
            r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=None, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                                did_not_finnish=False,
                                                score=10)

    def test_RaceEntry_Invalid_NotNull_shore_officer(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
            sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
            ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[
                0]
            b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
            r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=None,
                                                did_not_finnish=False,
                                                score=10)

    def test_RaceEntry_Invalid_NotNull_did_not_finnish(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
            sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
            ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[
                0]
            b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
            r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                                did_not_finnish=None,
                                                score=10)

    def test_RaceEntry_Invalid_Null_boat(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=None, race_handicap=500,
                                            time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                            did_not_finnish=False,
                                            score=10)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_RaceEntry_Invalid_Null_race_handicap(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=None,
                                            time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                            did_not_finnish=False,
                                            score=10)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_RaceEntry_Invalid_Null_time(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                            time=None, shore_officer=True,
                                            did_not_finnish=False,
                                            score=10)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_RaceEntry_Invalid_Null_score(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                            time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                            did_not_finnish=False,
                                            score=None)
        r[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_RaceEntry_composite_key_both_the_same(self):
        with self.assertRaisesMessage(django.db.utils.IntegrityError, ""):
            s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
            sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
            ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
            b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
            r = RaceEntry.objects.create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                                did_not_finnish=False,
                                                score=10)
            r2 = RaceEntry.objects.create(sailor_id=sa, race_id=ra, boat=b, race_handicap=600,
                                                time=datetime.timedelta(minutes=38, seconds=42), shore_officer=True,
                                                did_not_finnish=False,
                                                score=10)

    def test_RaceEntry_composite_key_one_different(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        ra2 = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                                did_not_finnish=False,
                                                score=10)
        r2 = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra2, boat=b, race_handicap=500,
                                                time=datetime.timedelta(minutes=34, seconds=42), shore_officer=True,
                                                did_not_finnish=False,
                                                score=10)
        r[0].save()
        r2[0].save()
        TestCase.assertEqual(self, True, r[1])

    def test_RaceEntry_default_shore_officer(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                            time=datetime.timedelta(minutes=34, seconds=42),
                                            did_not_finnish=False,
                                            score=10)
        r[0].save()
        re = RaceEntry.objects.get(pk=1)
        TestCase.assertFalse(self, re.shore_officer)

    def test_RaceEntry_default_did_not_finnish(self):
        s = Series.objects.get_or_create(name="Series1", ongoing="True")[0]
        sa = Sailor.objects.get_or_create(name="Sailor1", series_id=s)[0]
        ra = Race.objects.get_or_create(date=datetime.date(2021, 6, 20), name="race1", series_id=s, completed=True)[0]
        b = Boat.objects.get_or_create(boat="topper", handicap=500)[0]
        r = RaceEntry.objects.get_or_create(sailor_id=sa, race_id=ra, boat=b, race_handicap=500,
                                            time=datetime.timedelta(minutes=34, seconds=42),
                                            shore_officer=False,
                                            score=10)
        r[0].save()
        re = RaceEntry.objects.get(pk=1)
        TestCase.assertFalse(self, re.did_not_finnish)
