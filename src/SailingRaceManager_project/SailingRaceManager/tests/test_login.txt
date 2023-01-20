from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib import auth
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

    def test_login_works(self):

        response = self.c.post(reverse("SailingRaceManager:login"), {"username": "admin", "password": "1234"})
        print(response)

        TestCase.assertTrue(self, auth.get_user(self.client).is_authenticated)
