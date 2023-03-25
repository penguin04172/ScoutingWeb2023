from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
def MainPage(request):
    events = list(Event.objects.all())
    return render(request, 'index.html', {
        'eventList': events
    })

def EventPage(request, event):
    if (Event.objects.filter(id=event).first() == None):
        return HttpResponseRedirect('/')
    eventData = Event.objects.get(id=event)
    matchList = list(Match.objects.filter(event_id=event).all())
    teamList = list(Team.objects.filter(event_id=event).all())
    return render(request, 'event.html', {
        'selEvent': event,
        'eventData': eventData,
        'matchList': matchList,
        'teamList': teamList
    })

def TeamPage(request, event, num):
    teamData = Team.objects.get(id=f'{event}_{num}')
    overview = {
        'matchCount': 0,
        'scoreMax': 0,
        'scoreAvg': 0,
        'rp': 0,
        'rs': 0,
        'opr': 0
    }
    allData = {
        'scoreList': [],
        'rankList': [],
        'oprList': [],
        'autoList': [],
        'startList': [],
        'teleList': [],
        'gridList': [],
        'pickList': [],
        'autoDockList': [],
        'teleDockList': [],
        'cycleList': [],
        'dockTimerList': [],
        'autoPlaceList': [[], [], []],
        'telePlaceList': [[], [], []],
    }
    scoreData = {
        'autoMax': 0,
        'autoAvg': 0,
        'autoPlace': [0, 0, 0],
        'autoDock': [0, 0, 0],
        'teleMax': 0,
        'teleAvg': 0,
        'teleCycle': 0,
        'telePickMax': 0,
        'telePlaceMax': [0, 0, 0],
        'telePlaceAvg': [0, 0, 0],
        'telePlaceSuc': [0, 0, 0],
        'teleDock': [0, 0, 0, 0],
        'teleDockTime': 0,
    }

    for score in teamData.scores.all():
        allData['scoreList'].append(score.score_total)
        allData['startList'].append(score.start)
        allData['autoList'].append(score.score_auto)
        allData['teleList'].append(score.score_tele)
        allData['gridList'].append(score.grid_as_list())
        allData['pickList'].append(score.pick_as_dict())
        allData['autoDockList'].append(score.auto_dock)
        allData['teleDockList'].append(score.end_dock)
        allData['cycleList'].extend(score.cycle_as_list())
        allData['dockTimerList'].append(float(score.timer_dock))

    for sys in teamData.sysScore.all():
        allData['rankList'].append(sys.rank)

    for grid in allData['gridList']:
        for i in range(3):
            allData['autoPlaceList'][i].append(grid[i*9:i*9+9].count(1) + grid[i*9:i*9+9].count(2))
            allData['telePlaceList'][i].append(grid[i*9:i*9+9].count(3) + grid[i*9:i*9+9].count(4))
    
    overview['matchCount'] = teamData.scores.all().count()
    overview['scoreMax'] = max(allData['scoreList'])
    overview['scoreAvg'] = sum(allData['scoreList']) / len(allData['scoreList'])
    overview['rp'] = sum(allData['rankList'])
    overview['rs'] = sum(allData['rankList']) / (len(allData['rankList']) if len(allData['rankList']) else 1)
    
    scoreData['autoMax'] = max(allData['autoList'])
    scoreData['autoAvg'] = sum(allData['autoList'])/len(allData['autoList'])
    scoreData['teleMax'] = max(allData['teleList'])
    scoreData['teleAvg'] = sum(allData['teleList'])/len(allData['teleList'])



    return render(request, 'team.html', {
        'teamData': teamData,
        'overview': overview,
        'scoreData': scoreData
    })

def MatchPage(request, event, level, num):
    return render(request, 'match.html', {

    })

def ScoutPage(request, event, level, num, side):
    matchData = Match.objects.get(id=f'{event}_{level}_{num}')
    scoutList = list(SuperScout.objects.filter(match_id=f'{event}_{level}_{num}').all())
    systemData = SystemScoring.objects.get(id=f'{event}_{level}_{num}_{side}')
    teamList = matchData.teams_as_list()

    if side == 'blue':
        scoutList = scoutList[0:3]
        teamList = teamList[0:3]
    elif side == 'red':
        scoutList = scoutList[3:6]
        teamList = teamList[3:6]

    if request.method == 'POST':
        try:
            for i in range(3):
                team = Team.objects.filter(id=f'{event}_{teamList[i]}').first()
                if (team != None):
                    scoutList[i].team = team
                    systemData.team.add(team)
                scoutList[i].scouter = request.POST.get('scouter')
                scoutList[i].quick = request.POST.getlist('quick')[i]
                scoutList[i].defence = request.POST.getlist('defence')[i]
                scoutList[i].aware = request.POST.getlist('aware')[i]
                scoutList[i].human = request.POST.getlist('human')[i]
                scoutList[i].pick = request.POST.getlist('pick')[i]
                scoutList[i].place = request.POST.getlist('place')[i]
                scoutList[i].foul = request.POST.getlist('foul')[i]
                scoutList[i].other = request.POST.getlist('other')[i]
                scoutList[i].save()

            systemData.mobility = request.POST.get('mobility')
            systemData.grid = request.POST.get('grid')
            systemData.charge = request.POST.get('charge')
            systemData.penalty = request.POST.get('penalty')
            systemData.total = request.POST.get('total')
            systemData.rank = request.POST.get('rank')
            systemData.save()
        except:
            return HttpResponseBadRequest()
        return HttpResponseRedirect(f'/data/{event}/')

    return render(request, 'scout.html', {
        'matchData': matchData,
        'systemData': systemData,
        'scoutList': scoutList,
        'side': side,
    })

def RecordPage(request, event, level, num, robot):
    matchData = Match.objects.get(id=f'{event}_{level}_{num}')
    if robot == 6:
        if request.method == 'POST':
            record = MatchData.objects.get(id=request.POST.get('id'))

            if (Team.objects.filter(id=f'{event}_{request.POST.get("team")}').first() != None):
                record.team_data.id = f'{event}_{request.POST.get("team")}'

            record.scouter = request.POST.get('scouter')
            record.team = int(request.POST.get('team'))
            record.robot = int(request.POST.get('robot'))
            record.start = int(request.POST.get('start'))
            record.auto_grid = request.POST.get('auto_grid')
            record.tele_grid = request.POST.get('tele_grid')
            record.cross_cable = request.POST.get('cross_cable')!=None
            record.cross_charge = request.POST.get('cross_charge')!=None
            record.auto_mobility = request.POST.get('auto_mobility')!=None
            record.auto_dock = int(request.POST.get('auto_dock'))
            record.timer_cycle = request.POST.get('timer_cycle')
            record.tele_trans = int(request.POST.get('tele_trans'))
            record.tele_fed = request.POST.get('tele_fed')!=None
            record.tele_defender = request.POST.get('tele_defender')
            record.tele_pick_sn = request.POST.get('tele_pick_sn')
            record.tele_pick_fn = request.POST.get('tele_pick_fn')
            record.tele_pick_sb = request.POST.get('tele_pick_sb')
            record.tele_pick_fb = request.POST.get('tele_pick_fb')
            record.tele_fail = int(request.POST.get('tele_fail'))
            record.timer_dock = request.POST.get('timer_dock')
            record.end_dock = int(request.POST.get('end_dock'))
            record.other_link = request.POST.get('other_link')
            record.other_immobolity = request.POST.get('other_immobolity')!=None
            record.other_tippy = request.POST.get('other_tippy')!=None
            record.other_comment = request.POST.get('other_comment')
            record.score_auto = int(request.POST.get('score_auto'))
            record.score_tele = int(request.POST.get('score_tele'))
            record.score_link = int(request.POST.get('score_link'))
            record.score_dock = int(request.POST.get('score_dock'))
            record.score_grid = int(request.POST.get('score_grid'))
            record.score_total = int(request.POST.get('score_total'))
            record.save()

            return HttpResponseRedirect(f'/data/{event}/')
        return render(request, 'record.html', {
            'matchData': matchData,
        })
    scoreData = MatchData.objects.get(id=f'{event}_{level}_{num}_{robot}')
    scoutData = SuperScout.objects.get(id=f'{event}_{level}_{num}_{robot}')
    return render(request, 'result.html', {
            'matchData': matchData,
            'scoreData': scoreData,
            'scoutData': scoutData,
    })

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return HttpResponseRedirect('/')


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):
        matchId = f'{request.POST.get("event_id")}_{request.POST.get("level")}_{request.POST.get("num")}'
        Match.objects.create(
            id=matchId,
            level=int(request.POST.get("level")),
            num=int(request.POST.get("num")),
            teams=','.join(request.POST.getlist("teams")),
            event_id=request.POST.get("event_id")
        )
        for i in range(6):
            MatchData.objects.create(
                match_id=matchId,
                id = f'{matchId}_{i}'
            )
            place = (i%3) +1
            SuperScout.objects.create(
                match_id=matchId,
                id = f'{matchId}_{i}',
                quick = place,
                defence = place,
                aware = place,
                human = place,
                pick = place,
                place = place,
            )
        SystemScoring.objects.create(
            match_id = matchId,
            id = f'{matchId}_blue',
            red = False,
        )
        SystemScoring.objects.create(
            match_id = matchId,
            id = f'{matchId}_red',
            red = True,
        )
        
        return HttpResponseRedirect(f'/data/{request.POST.get("event_id")}/')
    

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        teamNum = request.POST.get('num')
        teamId = f'{request.POST.get("event_id")}_{teamNum}'
        team = Team.objects.create(
            id = teamId,
            num = int(teamNum),
            name = request.POST.get('name'),
            event_id = request.POST.get('event_id')
        )

        matchList = Match.objects.filter(event_id=request.POST.get('event_id')).all()
        for match in matchList:
            teams = match.teams.split(',')
            if teamNum in teams:
                teamIdx = teams.index(teamNum)

                score = list(match.scores.all())[teamIdx]
                score.team_data = team
                score.save()

                scout = list(match.scouts.all())[teamIdx]
                scout.team = team
                score.save()

        return HttpResponseRedirect(f'/data/{request.POST.get("event_id")}/')