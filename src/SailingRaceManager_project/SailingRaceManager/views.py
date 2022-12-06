from django.shortcuts import render
from django.http import HttpResponse
from SailingRaceManager.models import *


def index(request):
    # Query the database for lists of sailors in order of score in each siris with the ongoing flag set,
    # only including raced marked as completed
    series_s = Series.objects.filter(ongoing=True)
    leaderboards = []
    for s in series_s:
        race_entries = RaceEntry.objects.filter(race_id__completed=True)
        sailors = Sailor.objects.filter(series_id=s.pk)
        leaderboard = []
        for sailor in sailors:
            total_score = 0
            races = race_entries.filter(sailor_id=sailor.pk)
            for r in races:
                total_score += r.score
            leaderboard.append({"name": sailor.name, "score": total_score})

        sorted_leaderboard = sorted(leaderboard, key=lambda d: d["score"])
        leaderboards.append({"name": s.name, "leaderboard": sorted_leaderboard})

    context_dict = {"leaderboards": leaderboards}
    return render(request, 'SailingRaceManager/leaderboard.html', context=context_dict)
