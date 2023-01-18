from django.urls import path
from SailingRaceManager import views

app_name = 'SailingRaceManager'

urlpatterns = [
path('', views.index, name='leaderboard'),
path('old-series/<slug:series_slug>/', views.old_series, name='old_series'),
path('login/', views.admin_login, name='login'),
path('admin-home/', views.admin_home, name='admin_home'),
path('logout/', views.admin_logout, name='logout'),
path('change-password/', views.change_password, name='change_password'),

]