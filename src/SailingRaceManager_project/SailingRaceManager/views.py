from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
    series_s = Series.objects.filter(completed=False)
    old_series_s = Series.objects.filter(completed=True)
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
            return HttpResponse(form.errors)

    else:
        context_dict = {"form": NewSeriesForm()}

        # retrieve ongoing series nand add to context dict
        ongoing_series_list = []
        series_s = Series.objects.filter(completed=False)
        if len(series_s) > 0:
            for s in series_s:
                ongoing_series_list.append(s)

            context_dict["ongoing_series"] = ongoing_series_list
        else:
            context_dict["ongoing_series"] = None

        # retrieve old series
        old_series_list = []
        old_series_s = Series.objects.filter(completed=True)
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
    # handle post requests
    if request.method == 'POST':

        if request.POST.get("command") == "delSeries":
            try:
                series = Series.objects.get(slug=series_slug)
                series.delete()

            except Series.DoesNotExist:
                pass

            return HttpResponse(reverse("SailingRaceManager:admin_home"))

        elif request.POST.get("command") == "updateCompleted":
            try:
                series = Series.objects.get(slug=series_slug)
                val = request.POST.get("val")
                series.completed = (val == "true")
                series.save()

            except Series.DoesNotExist:
                return HttpResponse("Series Error")

            return HttpResponse("success")

        elif request.POST.get("command") == "updateOption":
            try:
                series = Series.objects.get(slug=series_slug)
                val = request.POST.get("val")
                option = request.POST.get("option")

                if option == "DNC":
                    series.DNCscore = val
                elif option == "DNF":
                    series.DNFscore = val
                else:
                    series.SOscore = val
                series.save()

            except Series.DoesNotExist:
                return HttpResponse("Series Error")

            return HttpResponse("success")

        elif request.POST.get("command") == "updateRace":
            try:
                series = Series.objects.get(slug=series_slug)
                race = Race.objects.filter(series_id=series)[int(request.POST.get("row"))]
                col = request.POST.get("col")
                if col == "0":
                    race.name = request.POST.get("val")
                    race.save()
                elif col == "1":
                    race.date = datetime.datetime.strptime(request.POST.get("val").split(" ")[0], "%Y-%m-%d")
                    race.save()
                    pass
                elif col == "2":
                    val = request.POST.get("val")
                    race.completed = (val == "true")
                    race.save()
                else:
                    raise IndexError

            except Series.DoesNotExist:
                return HttpResponse("Series Error")
            except IndexError:
                return HttpResponse("Col Error")

            return HttpResponse("success")

        elif request.POST.get("command") == "addRace":
            series = Series.objects.get(slug=series_slug)
            race = Race.objects.create(name="Enter Name", date=datetime.datetime.today().strftime('%Y-%m-%d'),
                                       completed=False, series_id=series)
            race.save()
            return HttpResponse("success")

        elif request.POST.get("command") == "delRace":
            try:
                series = Series.objects.get(slug=series_slug)
                race = Race.objects.filter(series_id=series)[int(request.POST.get("row"))]
                race.delete()
            except Series.DoesNotExist:
                return HttpResponse("Series Error")

            return HttpResponse("success")

        elif request.POST.get("command") == "openEditor":
            try:
                series = Series.objects.get(slug=series_slug)
                race = Race.objects.filter(series_id=series)[int(request.POST.get("row"))]

            except Series.DoesNotExist:
                return HttpResponse("Series Error")
            except Race.DoesNotExist:
                return HttpResponse("Series Error")

            return HttpResponse(reverse("SailingRaceManager:admin_race_editor", args=[race.slug]))

        elif request.POST.get("command") == "updateSailor":
            try:
                series = Series.objects.get(slug=series_slug)
                sailor = Sailor.objects.filter(series_id=series)[int(request.POST.get("row"))]
                sailor.name = request.POST.get("val")
                sailor.save()

            except Series.DoesNotExist:
                return HttpResponse("Series Error")

            return HttpResponse("success")

        elif request.POST.get("command") == "addSailor":
            series = Series.objects.get(slug=series_slug)
            sailor = Sailor.objects.create(name="Enter Name", series_id=series)
            sailor.save()
            return HttpResponse("success")

        elif request.POST.get("command") == "delSailor":
            try:
                series = Series.objects.get(slug=series_slug)
                sailor = Sailor.objects.filter(series_id=series)[int(request.POST.get("row"))]
                sailor.delete()
            except Series.DoesNotExist:
                return HttpResponse("Series Error")

            return HttpResponse("success")

    # handle get requests
    context_dict = {"slug": series_slug}
    try:
        series = Series.objects.get(slug=series_slug)
        context_dict["completed"] = json.dumps(series.completed)
        context_dict["DNCscore"] = json.dumps(series.DNCscore)
        context_dict["DNFscore"] = json.dumps(series.DNFscore)
        context_dict["SOscore"] = json.dumps(series.SOscore)

        races = Race.objects.filter(series_id=series)
        race_data = []
        for r in races:
            race_data.append([r.name, r.date.strftime('%Y/%m/%d'), str(r.completed).lower()])

        context_dict["json_races"] = json.dumps(race_data)

        sailors = Sailor.objects.filter(series_id=series)
        sailor_data = []
        for s in sailors:
            sailor_data.append([s.name])

        context_dict["json_sailors"] = json.dumps(sailor_data)

        context_dict["json_leaderboard"] = json.dumps(get_leaderboard_summery(series))

    except Series.DoesNotExist:
        context_dict["json_races"] = None
        context_dict["json_sailors"] = None

    return render(request, "SailingRaceManager/admin_series_editor.html", context_dict)


@login_required
def race_editor(request, race_slug):
    # handle post requests
    if request.method == 'POST':
        if request.POST.get("command") == "updateRaceEntry":
            try:
                race = Race.objects.get(slug=race_slug)
                raceEntry = RaceEntry.objects.filter(race_id=race)[int(request.POST.get("row"))]
                col = request.POST.get("col")
                if col == "1":
                    raceEntry.boat = Boat.objects.get(boat=request.POST.get("val"))
                    raceEntry.race_handicap = raceEntry.boat.handicap
                    raceEntry.save()
                elif col == "2":
                    old_time_s = raceEntry.time.seconds % 60
                    time_m = int(request.POST.get("val"))
                    raceEntry.time = datetime.timedelta(seconds=old_time_s, minutes=time_m)
                    raceEntry.save()
                elif col == "3":
                    time_s = int(request.POST.get("val"))
                    old_time_m = raceEntry.time.seconds // 60
                    raceEntry.time = datetime.timedelta(seconds=time_s, minutes=old_time_m)
                    raceEntry.save()
                elif col == "5":
                    val = request.POST.get("val")
                    raceEntry.did_not_finish = (val == "true")
                    raceEntry.save()
                elif col == "6":
                    val = request.POST.get("val")
                    raceEntry.shore_officer = (val == "true")
                    raceEntry.save()
                else:
                    raise IndexError

                new_time = time_to_string(raceEntry.corrected_time)
                return JsonResponse({"time": new_time, "handicap": raceEntry.boat.handicap})

            except Series.DoesNotExist:
                return HttpResponse("Series Error")
            except IndexError:
                return HttpResponse("Col Error")

    # handle get requests
    context_dict = {"slug": race_slug}
    try:
        race = Race.objects.get(slug=race_slug)

        raceEntries = RaceEntry.objects.filter(race_id=race)
        raceEntries_data = []
        for re in raceEntries:
            time_m = (re.time.seconds // 60)
            time_s = (re.time.seconds % 60)
            corrected_time = time_to_string(re.corrected_time)

            if re.boat == None:
                boat = None
                handicap = None
            else:
                boat = re.boat.boat
                handicap = re.boat.handicap


            raceEntries_data.append(
                [re.sailor_id.name, boat, time_m, time_s, handicap,
                 re.did_not_finish, re.shore_officer,
                 corrected_time])

        context_dict["json_raceEntries"] = json.dumps(raceEntries_data)

        boats = Boat.objects.all()
        boats_data = []
        for b in boats:
            boats_data.append(b.boat)

        context_dict["json_boats"] = json.dumps(boats_data)

    except Race.DoesNotExist:
        context_dict["json_raceEntries"] = None

    return render(request, "SailingRaceManager/admin_race_editor.html", context_dict)


# ---------------helper functions------------------------

# Helper function to get the sorted leaderboard of sailors from the given series
def get_leaderboard(s):
    race_entries = RaceEntry.objects.filter(race_id__completed=True)
    sailors = Sailor.objects.filter(series_id=s.pk)
    leaderboard = []

    for sailor in sailors:
        total_score = 0
        # races = race_entries.filter(sailor_id=sailor.pk)
        # for r in races:
        #    total_score += r.corrected_time.
        leaderboard.append({"name": sailor.name, "score": total_score})

    return sorted(leaderboard, key=lambda d: d["score"])


def get_leaderboard_summery(s):
    leaderboard = []
    races = []
    sailors = Sailor.objects.filter(series_id=s.pk)
    for race in Race.objects.filter(series_id=s.pk, completed=True):
        races.append(race.name)

        times = []
        for re in RaceEntry.objects.filter(race_id = race):
            times.append({"entry":re.pk,"score":re.corrected_time})
        times = sorted(times, key=lambda d: d["score"])
        score = 1
        for re in times:
            if RaceEntry.objects.get(pk=re["entry"]).did_not_finish:
                re["score"] = Series.objects.get(pk=s).DNFscore
            elif RaceEntry.objects.get(pk=re["entry"]).shore_officer:
                re["score"] = Series.objects.get(pk=s).SOscore
            elif RaceEntry.objects.get(pk=re["entry"]).corrected_time == "0m 0s":
                re["score"] = Series.objects.get(pk=s).DNCscore
            else:
                re["score"] = score
                score += 1

        for sailor in sailors:
            raceEntries = RaceEntry.objects.filter(race_id__completed=True).filter(sailor_id=sailor.pk)
            result = [s.name]
            for r in raceEntries:
                result.append(time_to_string(r.corrected_time))

            for re in times:
                if re["entry"] == sailor.pk:
                    result.append(re["score"])

            leaderboard.append(result)



    sailors = Sailor.objects.filter(series_id=s.pk)
    for sailor in sailors:
        raceEntries = RaceEntry.objects.filter(race_id__completed=True).filter(sailor_id=sailor.pk)
        result = [s.name]
        for r in raceEntries:
            result.append(time_to_string(r.corrected_time))
        leaderboard.append(result)




    return [leaderboard, races]


def time_to_string(time):
    return "{}m {}s".format((time.seconds // 60), (time.seconds % 60))
