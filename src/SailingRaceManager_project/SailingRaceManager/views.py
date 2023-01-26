from django.shortcuts import render
from django.http import HttpResponse
from SailingRaceManager.models import *
from SailingRaceManager.forms import NewSeriesForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.urls import reverse
from django.shortcuts import redirect
import json
import datetime


# Leaderboard page, Called index as acts as the index page for the website.
def index(request):
    # Query the database for lists of sailors, in order of score, in each series with the ongoing flag set
    # Query the database for list of series that have the ongoing flag not set
    # only including races marked as completed
    series_s = Series.objects.filter(ongoing=True)
    old_series_s = Series.objects.filter(ongoing=False)
    leaderboards = []
    context_dict = {}

    # query info from ongoing series and add to context dict
    if len(series_s) > 0:
        for s in series_s:
            sorted_leaderboard = get_leaderboard(s)
            leaderboards.append({"name": s.name, "leaderboard": sorted_leaderboard})

        context_dict["leaderboards"] = leaderboards
    else:
        context_dict["leaderboards"] = None

    # add past series to context dict
    if len(old_series_s) > 0:
        old_series_list = []
        for old_s in old_series_s:
            old_series_list.append(old_s)
        context_dict["old_series"] = old_series_list
    else:
        context_dict["old_series"] = None

    return render(request, 'SailingRaceManager/leaderboard.html', context=context_dict)


# page for displaying old not ongoing series
def old_series(request, series_slug):
    context_dict = {}
    try:
        series = Series.objects.get(slug=series_slug)
        sorted_leaderboard = get_leaderboard(series)
        context_dict["series"] = {"name": series.name, "leaderboard": sorted_leaderboard}
    except Series.DoesNotExist:
        context_dict["series"] = None

    return render(request, 'SailingRaceManager/old_series.html', context=context_dict)


# view for admin homepage. only logged-in users can access
@login_required
def admin_home(request):
    if request.method == 'POST':
        form = NewSeriesForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("SailingRaceManager:admin_home"))
        else:
            print(form.errors)

    else:
        context_dict = {"form": NewSeriesForm()}

        # retrieve ongoing series nand add to context dict
        ongoing_series_list = []
        series_s = Series.objects.filter(ongoing=True)
        if len(series_s) > 0:
            for s in series_s:
                ongoing_series_list.append(s)

            context_dict["ongoing_series"] = ongoing_series_list
        else:
            context_dict["ongoing_series"] = None

        # retrieve old series
        old_series_list = []
        old_series_s = Series.objects.filter(ongoing=False)
        if len(old_series_s) > 0:
            for old_s in old_series_s:
                old_series_list.append(old_s)

            context_dict["old_series"] = old_series_list
        else:
            context_dict["old_series"] = None

        return render(request, 'SailingRaceManager/admin_home.html', context=context_dict)


# view for loging in to admin pages
def admin_login(request):
    if request.method == "POST":
        password = request.POST.get("password")

        # username is always admin on admin account
        user = authenticate(username="admin", password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("SailingRaceManager:admin_home"))
            else:
                return HttpResponse("Error, admin account disabled")
        else:
            return HttpResponse("Incorrect password")

    else:
        return render(request, "SailingRaceManager/admin_login.html")


@login_required
def admin_logout(request):
    logout(request)
    return redirect(reverse('SailingRaceManager:leaderboard'))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect(reverse("SailingRaceManager:change_password"))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "SailingRaceManager/change_password.html", {
        'form': form
    })


@login_required
def series_editor(request, series_slug):
    context_dict = {}
    try:
        series = Series.objects.get(slug=series_slug)
        races = Race.objects.filter(series_id=series)
        race_data = []
        for r in races:
            race_data.append({"name":r.name,"date":r.date,"completed":r.completed})
        context_dict["races"] = race_data
    except Series.DoesNotExist:
        context_dict["races"] = None

    return render(request, "SailingRaceManager/admin_series_editor.html")


# ---------------helper functions------------------------

# Helper function to get the sorted leaderboard of sailors from the given series
def get_leaderboard(s):
    race_entries = RaceEntry.objects.filter(race_id__completed=True)
    sailors = Sailor.objects.filter(series_id=s.pk)
    leaderboard = []

    for sailor in sailors:
        total_score = 0
        races = race_entries.filter(sailor_id=sailor.pk)
        for r in races:
            total_score += r.score
        leaderboard.append({"name": sailor.name, "score": total_score})

    return sorted(leaderboard, key=lambda d: d["score"])
