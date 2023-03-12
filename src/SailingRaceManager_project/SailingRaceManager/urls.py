from django.urls import path
from SailingRaceManager import views

app_name = 'SailingRaceManager'

urlpatterns = [
    path('', views.index, name='leaderboard'),
    path('old-series/<slug:series_slug>/', views.old_series, name='old_series'),
    path('login/', views.admin_login, name='login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('logout/', views.admin_logout, name='logout'),
    path('admin-home/change-password/', views.change_password, name='change_password'),
    path('admin-home/series-editor/<slug:series_slug>', views.series_editor, name='admin_series_editor'),
    path('admin-home/race-editor/<slug:race_slug>', views.race_editor, name='admin_race_editor'),
    path('admin-home/hanicap-editor/', views.handicap_editor, name='admin_handicap_editor'),
]
