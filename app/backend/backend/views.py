# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from backend.models import Teams, Solves, Challenges, Notices, Config, Wrong_keys, Hints, Registers, Index
from django.middleware.csrf import get_token
from django.utils.html import escape
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import time
from datetime import timedelta
import json
import hashlib

def ctftime(no_start = 0, no_end = 0):
    """ Checks whether it's CTF time or not. """
    start = time.mktime((Config.objects.all()[0].start_time + timedelta(hours = 8)).timetuple()) if not no_start else None
    end = time.mktime((Config.objects.all()[0].end_time + timedelta(hours = 8)).timetuple()) if not no_end else None
    if start and end:
        if start < time.time() < end:
            # Within the two time bounds
            return True
    if start < time.time() and end is None: 
        # CTF starts on a date but never ends
        return True
    if start is None and time.time() < end: 
        # CTF started but ends at a date
        return True
    if start is None and end is None:
        # CTF has no time requirements
        return True
    return False

def get_value(chalid, bouns = 0):
    i = Solves.objects.filter(chal = chalid).count()
    count = i if i else 1
    initial_value = Challenges.objects.get(id = chalid).value
    real_value = int(initial_value) * (1.0 / (0.1 * (count + 9.0))) * (1 + bouns)
    return real_value

def is_login(request):
    if request.session.get('team_id', False):
        return True
    return False

def check_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def get_csrf_token(request):
    return JsonResponse({"token": get_token(request)})

def register(request):
    req = json.loads(request.body)
    if not check_email(req['email']):
        return JsonResponse({"code": 0, "message": "Email is illegal"})
    if Teams.objects.filter(name = req['name']).count() or Teams.objects.filter(email = req['email']).count():
        return JsonResponse({"code": 0, "message": "Team name or email already exists."})
    registered = Registers.objects.filter(ip = request.META.get('REMOTE_ADDR'))
    if registered.count():
        if int(time.time() - registered[0].time) < 60:
            return JsonResponse({"code": 0, "message": "Can only be registered once per minute."})
        else:
            registered.update(time = int(time.time()))
    else:
        Registers.objects.create(ip = request.META.get('REMOTE_ADDR'), time = int(time.time()))
    Teams.objects.create(name = req['name'], email = req['email'], password = hashlib.md5(req['password']).hexdigest(), school = req['school'])
    return JsonResponse({"code": 1, "message": "Register successful."})

def login(request):
    req = json.loads(request.body)
    res = {"code": 0, "message": "Login failed."}
    if not Teams.objects.filter(name = req['name']).count():
        return JsonResponse(res)
    team = Teams.objects.get(name = req['name'])
    password = hashlib.md5(req['password']).hexdigest()
    if team.password == password:
        request.session['team_id'] = team.id
        return JsonResponse({"code": 1, "message": "Login successful.", "team_id": team.id})
    else:
        return JsonResponse(res)

def logout(request):
    if request.session.get('team_id', False):
        del request.session["team_id"]
        return JsonResponse({"code": 1, "message": "Logout successful."})

def get_all(request):
    if not is_login(request):
        return JsonResponse({"code": 0, "message":  "You are not logged in."})
    if not ctftime(no_end = 1):
        del request.session["team_id"]
        return JsonResponse({"code": 0, "message":  "The game has not yet begun or has ended."})
    notices = Notices.objects.all()
    challenges = Challenges.objects.select_related().filter(show = 1)
    res = {}
    res[0] = {
        "type": "notice",
        "avatar": '../../' + str(Config.objects.all()[0].official_avatar),
        "title": u"官方公告",
        "text": [],
        "done": 1
    }
    for notice in notices.iterator():
        res[0]["text"].append(escape(notice.content).replace("\n", "<br>"))
    for challenge in challenges.iterator():
        res[challenge.id] = {
            "type": challenge.category,
            "avatar": '../../' + str(challenge.author.avatar),
            "title": challenge.name,
            "text": [u"题目描述：<br>" + escape(challenge.description).replace("\n", "<br>"), u"题目分值：%.2f" % get_value(challenge.id), u"被解出次数：" + str(Solves.objects.filter(chal = challenge).count())],
            "done": 1 if Solves.objects.filter(chal = challenge, team = request.session['team_id']).count() else 0
        }
        hints = Hints.objects.filter(chal = challenge)
        if hints.count():
            i = 1
            for hint in hints.iterator():
                res[challenge.id]["text"].append("hint{}: {}".format(str(i), escape(hint.content).replace("\n", "<br>")))
                i += 1
    return JsonResponse(res)

def submit(request):
    if not is_login(request):
        return JsonResponse({"code": 0, "message":  "You are not logged in."})
    if not ctftime():
        return JsonResponse({"code": 0, "message":  "The game has not yet begun or has ended."})
    req = json.loads(request.body)
    challenge = Challenges.objects.get(id = req['id'])
    team = Teams.objects.get(id = request.session['team_id'])
    if Solves.objects.filter(chal = challenge, team = team).count():
        return JsonResponse({"code": 0, "message": "You have solved this problem."})
    if Wrong_keys.objects.filter(chal = challenge, team = team).count() >= 100:
        return JsonResponse({"code": 0, "message": "You have reached the maximum number of submissions."})
    if req['flag'] == challenge.flag:
        if not Solves.objects.filter(chal = challenge).count():
            Notices.objects.create(content = "Congratulations to {} for getting the first blood of {}!".format(team.name, challenge.name))
        Solves.objects.create(chal = challenge, team = team, value = challenge.value, ip = request.META.get('REMOTE_ADDR'), bouns = eval(challenge.bouns)[str(Solves.objects.filter(chal = challenge).count())] if Solves.objects.filter(chal = challenge).count() < len(eval(challenge.bouns)) else "0")
        return JsonResponse({"code": 1, "message": "Congratulations! Your flag is correct."})
    else:
        Wrong_keys.objects.create(chal = challenge, team = team, flag = req['flag'], ip = request.META.get('REMOTE_ADDR'))
        return JsonResponse({"code": 0, "message": "Your flag is incorrect."})

def get_score(request):
    req = json.loads(request.body)
    challenge = Challenges.objects.filter(id = req["id"]).count()
    return JsonResponse({"code": 1, "score": "%.2f" % get_value(req["id"])}) if challenge else JsonResponse({"code": 0, "score": "No such challenge"})

def scoreboard(request, http = 1):
    solves = Solves.objects.select_related().all()
    teams = {}
    for solve in solves.iterator():
        if solve.team.id not in teams:
            teams[solve.team.id] = {"id": solve.team.id, "name": solve.team.name, "score": get_value(solve.chal.id, float(solve.bouns)), "date": time.mktime(solve.date.timetuple())}
        else:
            teams[solve.team.id]["score"] += get_value(solve.chal.id, float(solve.bouns))
            teams[solve.team.id]["date"] = time.mktime(solve.date.timetuple()) if time.mktime(solve.date.timetuple()) > teams[solve.team.id]["date"] else teams[solve.team.id]["date"]
    teams = sorted(teams.items(), key = lambda k : (k[1]['date']))
    teams = sorted(teams, key = lambda k : (k[1]['score']), reverse = True)
    res = {}
    rank = 1
    for team in teams:
        team[1]['score'] = "%.2f" % team[1]['score']
        res[rank] = {"id": team[1]["id"], "name": team[1]["name"], "score": team[1]["score"]}
        rank += 1
    return JsonResponse(res) if http else res

def challenge_rank(request):
    challenges = Challenges.objects.filter(show = 1)
    tmp = []
    for challenge in challenges.iterator():
        tmp.append([challenge.name, challenge.category, get_value(challenge.id)])
    tmp = sorted(tmp, key = lambda k : (k[2]), reverse = True)
    res = {}
    rank = 1
    for i in tmp:
        i[2] = "%.2f" % i[2]
        res[rank] = {"name": i[0], "category": i[1], "score": i[2]}
        rank += 1
    return JsonResponse(res)

def teaminfo(request, team_id):
    if not Teams.objects.filter(id = team_id).count():
        return JsonResponse({"code": 0, "message":  "This team does not exist."})
    team = Teams.objects.get(id = team_id)
    solves = Solves.objects.select_related().filter(team = team)
    rank_info = scoreboard(request,  http = 0)
    res = {"name": team.name, "solves": [], "rank": 0, "score": 0}
    for solve in solves.iterator():
        res["solves"].append({"name": solve.chal.name, "category": solve.chal.category, "score": "%.2f" % get_value(solve.chal.id, float(solve.bouns)), "date": str(solve.date + timedelta(hours = 8))[:19]})
    for rank in rank_info:
        if rank_info[rank]["id"] == int(team_id):
            res["rank"] = rank
            res["score"] = rank_info[rank]["score"]
    return JsonResponse(res)

def get_index(request):
    if Index.objects.all().count():
        content = Index.objects.all()[0].content
    else:
        content = "Hello, world!"
    return JsonResponse({"code": 1, "content": content})

