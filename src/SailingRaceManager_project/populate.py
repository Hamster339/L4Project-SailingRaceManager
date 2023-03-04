import os
import django
import datetime

# python script to remove and recreate the database and populate it with test data

# setup django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SailingRaceManager_project.settings')
django.setup()
from SailingRaceManager.models import *


# function populates the database
def populate():
    # data to be poplated, foregn key fields are excluded
    series_data = [{"name": "2021", "ongoing": True},
                   {"name": "2022", "ongoing": False},
                   ]

    race_data = [{"date": datetime.date(2021, 6, 20), "name": "20th june", "completed": True},
                 {"date": datetime.date(2021, 7, 20), "name": "Final", "completed": True},
                 {"date": datetime.date(2022, 7, 1), "name": "First", "completed": True},
                 {"date": datetime.date(2022, 8, 1), "name": "open day", "completed": True},
                 {"date": datetime.date(2022, 9, 1), "name": "2022 series final", "completed": False}, ]

    sailor_data = [{"name": "Jim"},
                   {"name": "Jane"},
                   {"name": "Jim"},
                   {"name": "Jane"},
                   {"name": "Bill"}]

    handicap_data = [{"boat": "BRITISH MOTH", "number": 1160},
                     {"boat": "ILCA 7 / Laser ", "number": 1100},
                     {"boat": "TOPPER ", "number": 1365},
                     {"boat": "WAYFARER", "number": 1102},
                     ]

    race_entry_data = [
        {"time": datetime.timedelta(minutes=34, seconds=42), "shore_officer": False, "did_not_finish": False,
         "score": 1},
        {"time": datetime.timedelta(minutes=32, seconds=42), "shore_officer": False, "did_not_finish": False,
         "score": 2},
        {"time": datetime.timedelta(seconds=0), "shore_officer": False, "did_not_finish": False, "score": 50},
        {"time": datetime.timedelta(minutes=31, seconds=42), "shore_officer": False, "did_not_finish": False,
         "score": 1},
        {"time": datetime.timedelta(minutes=36, seconds=10), "shore_officer": False, "did_not_finish": False,
         "score": 2},
        {"time": datetime.timedelta(seconds=0), "shore_officer": True, "did_not_finish": False, "score": 10},
        {"time": datetime.timedelta(minutes=20, seconds=41), "shore_officer": False, "did_not_finish": False,
         "score": 1},
        {"time": datetime.timedelta(seconds=0), "shore_officer": False, "did_not_finish": True, "score": 20},
        {"time": datetime.timedelta(minutes=78, seconds=42), "shore_officer": False, "did_not_finish": False,
         "score": 1},
        {"time": datetime.timedelta(minutes=14, seconds=54), "shore_officer": False, "did_not_finish": False,
         "score": 2},
        {"time": datetime.timedelta(minutes=46, seconds=42), "shore_officer": False, "did_not_finish": False,
         "score": 1},
        {"time": datetime.timedelta(minutes=76, seconds=1), "shore_officer": False, "did_not_finish": False,
         "score": 2},
        {"time": datetime.timedelta(minutes=28, seconds=42), "shore_officer": False, "did_not_finish": False,
         "score": 3}]

    # series of loops to do the populating
    series_list = []
    for s in series_data:
        record = add_series(s.get("name"), s.get("ongoing"))
        series_list.append(record)

    race_list = []
    for i in range(0, 2):
        r = race_data[i]
        record = add_race(r.get("date"), r.get("name"), series_list[0], r.get("completed"))
        race_list.append(record)
    for i in range(2, 5):
        r = race_data[i]
        record = add_race(r.get("date"), r.get("name"), series_list[1], r.get("completed"))
        race_list.append(record)

    sailor_list = []
    for i in range(0, 2):
        sa = sailor_data[i]
        record = add_sailor(sa.get("name"), series_list[0])
        sailor_list.append(record)
    for i in range(2, 5):
        sa = sailor_data[i]
        record = add_sailor(sa.get("name"), series_list[1])
        sailor_list.append(record)

    handicap_list = []
    for h in handicap_data:
        record = add_boat(h.get("boat"), h.get("number"))
        handicap_list.append(record)


# helper funtions to add a record to the database tables
def add_series(name, completed):
    p = Series.objects.get_or_create(name=name, completed=completed)[0]
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


if __name__ == "__main__":
    # remove previous database if it exists
    print("clearing Database...")

    os.system("del db.sqlite3")

    # re-migrate database and setup default admin user
    os.system("python .\manage.py  makemigrations")
    os.system("python .\manage.py  migrate")
    os.environ.setdefault('DJANGO_SUPERUSER_USERNAME', 'admin')
    os.environ.setdefault('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
    os.environ.setdefault('DJANGO_SUPERUSER_PASSWORD', 'admin')
    os.system("python .\manage.py createsuperuser --noinput")

    # remove leftover migration files
    os.system("del \SailingRaceManager\migrations\\0*")
    print("database cleared")

    # populate new database
    print("Starting population script...")
    populate()
    print("Population script successful")
