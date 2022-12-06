from django.urls import path
from SailingRaceManager import views

app_name = 'SailingRaceManager'

urlpatterns = [
path('', views.index, name='leaderboard'),
]