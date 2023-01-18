from django.test import TestCase
from django.test import Client
from django.urls import reverse
import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SailingRaceManager_project.settings')
django.setup()
from SailingRaceManager.models import *
from django.contrib.auth.models import User


class Test_old_Series(TestCase):
    c = None
    user = None

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="admin", password="1234")

    def test_not_avalible_when_logged_out(self):
        response = self.c.get(reverse("SailingRaceManager:admin_home"))

        # code 302 means client has been redirected, which happens when accessing restricted resource
        TestCase.assertEqual(self, response.status_code, 302)

    def test_onging_series(self):
        add_series("series1 ", True)
        add_series("series2 ", True)
        add_series("series3 ", False)

        login = self.c.login(username="admin", password="1234")
        response = self.c.get(reverse("SailingRaceManager:admin_home"))

        TestCase.assertEqual(self, len(response.context["ongoing_series"]), 2)

    def test_past_series(self):
        add_series("series1 ", True)
        add_series("series2 ", True)
        add_series("series3 ", False)

        login = self.c.login(username="admin", password="1234")
        response = self.c.get(reverse("SailingRaceManager:admin_home"))

        TestCase.assertEqual(self, len(response.context["old_series"]), 1)


# helper functions to add things to the database
def add_series(name, ongoing):
    p = Series.objects.get_or_create(name=name, ongoing=ongoing)[0]
    p.save()
    return p
