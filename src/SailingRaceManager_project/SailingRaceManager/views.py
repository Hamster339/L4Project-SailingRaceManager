from django.shortcuts import render
from django.http import HttpResponse
from SailingRaceManager.models import *


def index(request):
    # Query the database for lists of sailors in order of score in each siris with the ongoing flag set,
    # only including raced marked as completed
    series_s = Series.objects.filter(ongoing=True)
    old_series_s = Series.objects.filter(ongoing=False)
    leaderboards = []
    context_dict = {}

    if len(series_s) > 0:
        for s in series_s:
            sorted_leaderboard = get_leaderboard(s)
            leaderboards.append({"name": s.name, "leaderboard": sorted_leaderboard})

        context_dict["leaderboards"] = leaderboards
    else:
        context_dict["leaderboards"] = None

    if len(old_series_s) > 0:
        old_series_list = []
        for old_s in old_series_s:
            old_series_list.append(old_s)
        context_dict["old_series"] = old_series_list
    else:
        context_dict["old_series"] = None

    return render(request, 'SailingRaceManager/leaderboard.html', context=context_dict)


def old_series(request, series_slug):
    context_dict = {}
    try:
        series = Series.objects.get(slug=series_slug)
        sorted_leaderboard = get_leaderboard(series)
        context_dict['series'] = {"name": series.name, "leaderboard": sorted_leaderboard}
    except Series.DoesNotExist:
        context_dict['series'] = None

    return render(request, 'SailingRaceManager/old_series.html', context=context_dict)

#helper functions
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