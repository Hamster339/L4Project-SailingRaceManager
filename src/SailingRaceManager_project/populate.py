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

    handicap_data = [{"boat": "420", "number": 1100},
                     {"boat": "2000", "number": 1114},
                     {"boat": "29ER", "number": 897},
                     {"boat": "505", "number": 900},
                     {"boat": "ALBACORE", "number": 1037},
                     {"boat": "ALTO", "number": 921},
                     {"boat": "B14", "number": 858},
                     {"boat": "BLAZE", "number": 1033},
                     {"boat": "BRITISH MOTH", "number": 1165},
                     {"boat": "BYTE CII", "number": 1135},
                     {"boat": "COMET", "number": 1210},
                     {"boat": "COMET TRIO (MK I)", "number": 1096},
                     {"boat": "COMET TRIO (MK II)", "number": 1052},
                     {"boat": "CONTENDER", "number": 969},
                     {"boat": "DEVOTI D-ONE", "number": 948},
                     {"boat": "DEVOTI D-ZERO", "number": 1029},
                     {"boat": "ENTERPRISE", "number": 1126},
                     {"boat": "EUROPE", "number": 1141},
                     {"boat": "FINN", "number": 1049},
                     {"boat": "FIREBALL", "number": 952},
                     {"boat": "FIREFLY", "number": 1174},
                     {"boat": "FLYING FIFTEEN", "number": 1021},
                     {"boat": "GP14", "number": 1133},
                     {"boat": "GRADUATE", "number": 1120},
                     {"boat": "HADRON H2", "number": 1038},
                     {"boat": "HORNET", "number": 959},
                     {"boat": "ICON", "number": 976},
                     {"boat": "ILCA 4 / Laser 4.7", "number": 1210},
                     {"boat": "ILCA 6 / Laser Radial", "number": 1150},
                     {"boat": "ILCA 7 / Laser", "number": 1101},
                     {"boat": "K1", "number": 1070},
                     {"boat": "K6", "number": 919},
                     {"boat": "KESTREL", "number": 1038},
                     {"boat": "LARK", "number": 1065},
                     {"boat": "LIGHTNING 368", "number": 1160},
                     {"boat": "MEGABYTE", "number": 1072},
                     {"boat": "MERLIN-ROCKET", "number": 980},
                     {"boat": "MIRACLE", "number": 1194},
                     {"boat": "MIRROR (D/H)", "number": 1387},
                     {"boat": "MIRROR (S/H)", "number": 1377},
                     {"boat": "MUSTO SKIFF", "number": 845},
                     {"boat": "NATIONAL 12", "number": 1064},
                     {"boat": "OK", "number": 1104},
                     {"boat": "OPTIMIST", "number": 1635},
                     {"boat": "OSPREY", "number": 934},
                     {"boat": "PHANTOM", "number": 1002},
                     {"boat": "ROOSTER 8.1", "number": 1035},
                     {"boat": "RS 100 8.4", "number": 1002},
                     {"boat": "RS 200", "number": 1046},
                     {"boat": "RS 300", "number": 965},
                     {"boat": "RS 400", "number": 940},
                     {"boat": "RS 500", "number": 966},
                     {"boat": "RS 600", "number": 920},
                     {"boat": "RS 700", "number": 845},
                     {"boat": "RS 800", "number": 799},
                     {"boat": "RS AERO 5", "number": 1136},
                     {"boat": "RS AERO 7", "number": 1063},
                     {"boat": "RS AERO 9", "number": 1010},
                     {"boat": "RS FEVA XL", "number": 1248},
                     {"boat": "RS TERA PRO", "number": 1364},
                     {"boat": "RS TERA SPORT", "number": 1445},
                     {"boat": "RS VAREO", "number": 1093},
                     {"boat": "RS VISION", "number": 1137},
                     {"boat": "SCORPION", "number": 1043},
                     {"boat": "SEAFLY", "number": 1071},
                     {"boat": "SOLO", "number": 1142},
                     {"boat": "SOLUTION", "number": 1096},
                     {"boat": "STREAKER", "number": 1128},
                     {"boat": "SUPERNOVA", "number": 1077},
                     {"boat": "TASAR", "number": 1017},
                     {"boat": "TOPPER", "number": 1369},
                     {"boat": "WANDERER", "number": 1193},
                     {"boat": "WAYFARER", "number": 1105}]

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
    os.system("del SailingRaceManager\migrations\\0*")
    print("database cleared")

    # populate new database
    print("Starting population script...")
    populate()
    print("Population script successful")
