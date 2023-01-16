from django.urls import path
from SailingRaceManager import views

app_name = 'SailingRaceManager'

urlpatterns = [
path('', views.index, name='leaderboard'),
path('old-series/<slug:series_slug>/', views.old_series, name='old_series'),
path('admin-login/', views.admin_login, name='admin_login'),
path('admin-home/', views.admin_home, name='admin_home'),

]