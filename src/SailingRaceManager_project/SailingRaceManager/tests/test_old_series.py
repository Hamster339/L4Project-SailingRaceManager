from django.test import TestCase
from django.test import Client
import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SailingRaceManager_project.settings')
django.setup()
from SailingRaceManager.models import *


class Test_old_Series(TestCase):
    c = None

    def setUp(self):
        self.c = Client()

    def test_current_series_number(self):
        add_series("Series 1", False)
        add_series("Series 2", False)
        slug = Series.objects.get(name="Series 1").slug

        response = self.c.get("/SailingRaceManager/old-series/" + slug + "/")
        TestCase.assertEqual(self, "Series 1", response.context["series"]["name"])


# helper functions to add things to the database
def add_series(name, ongoing):
    p = Series.objects.get_or_create(name=name, ongoing=ongoing)[0]
    p.save()
    return p
