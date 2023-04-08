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
        'grid': [],
        'autoMax': 0,
        'autoAvg': 0,
        'autoPlaceMax': [0, 0, 0],
        'autoPlaceAvg': [0, 0, 0],
        'autoDock': [0, 0, 0],
        'teleMax': 0,
        'teleAvg': 0,
        'teleCycle': 0,
        'telePickAll': 0,
        'telePickMax': 0,
        'telePickMaxItem': 0,
        'telePlaceMax': [0, 0, 0],
        'telePlaceAvg': [0, 0, 0],
        'telePlaceSuc': 0,
        'teleDock': [0, 0, 0, 0],
        'teleDockTime': 0,
    }
    scoutData = {
        'quick': 0,
        'defence': 0,
        'aware': 0,
        'human': 0,
        'pick': 0,
        'place': 0
    }
    commentData = {}
    for i in range(27):
        scoreData['grid'].append([0, 0])

    for score in teamData.scores.all():
        allData['scoreList'].append(score.score_total)
        allData['startList'].append(score.start)
        allData['autoList'].append(score.score_auto)
        allData['teleList'].append(score.score_tele)
        allData['gridList'].append(score.grid_as_list())
        allData['pickList'].append(score.pick_as_list())
        allData['autoDockList'].append(score.auto_dock)
        allData['teleDockList'].append(score.end_dock)
        allData['cycleList'].extend(score.cycle_as_list())
        allData['dockTimerList'].append(float(score.timer_dock) if score.timer_dock else 0)
        for g in list(map(int, score.auto_grid.split(',') if score.auto_grid != '' else [])):
            scoreData['grid'][g-9 if g>26 else g][0] += 1
        for g in list(map(int, score.tele_grid.split(',') if score.tele_grid != '' else [])):
            scoreData['grid'][g-9 if g>26 else g][1] += 1
        commentData[f'{score.match.level_as_str()}_{score.match.num}'] = [score.other_comment, '']

    for scout in teamData.scouts.all():
        scoutData['quick'] += scout.quick
        scoutData['defence'] += scout.defence
        scoutData['aware'] += scout.aware
        scoutData['human'] += scout.human
        scoutData['pick'] += scout.pick
        scoutData['place'] += scout.place
        commentData[f'{scout.match.level_as_str()}_{scout.match.num}'][1] = (scout.other)
    
    for key, data in scoutData.items():
        scoutData[key] = round(data / (teamData.scouts.all().count() if teamData.scouts.all().count() else 1), 2)

    for sys in teamData.sysScore.all():
        allData['rankList'].append(sys.rank)

    for grid in allData['gridList']:
        for i in range(3):
            allData['autoPlaceList'][i].append(grid[i*9:i*9+9].count(1) + grid[i*9:i*9+9].count(2))
            allData['telePlaceList'][i].append(grid[i*9:i*9+9].count(3) + grid[i*9:i*9+9].count(4))
    
    overview['matchCount'] = teamData.scores.all().count()
    if overview['matchCount'] > 0:
        overview['scoreMax'] = max(allData['scoreList'])
        overview['scoreAvg'] = round(sum(allData['scoreList']) / (overview['matchCount'] if overview['matchCount'] else 1), 2)
        overview['rp'] = sum(allData['rankList'])
        overview['rs'] = round(sum(allData['rankList']) / (overview['matchCount'] if overview['matchCount'] else 1), 2)
        
        scoreData['autoMax'] = max(allData['autoList'])
        scoreData['autoAvg'] = round(sum(allData['autoList']) / (overview['matchCount'] if overview['matchCount'] else 1), 2)
        scoreData['teleMax'] = max(allData['teleList'])
        scoreData['teleAvg'] = round(sum(allData['teleList']) / (overview['matchCount'] if overview['matchCount'] else 1), 2)



        for i in range(3):
            scoreData['autoPlaceMax'][i] = max(allData['autoPlaceList'][i])
            scoreData['autoPlaceAvg'][i] = round(sum(allData['autoPlaceList'][i]) / (overview['matchCount'] if overview['matchCount'] else 1), 2)
            scoreData['telePlaceMax'][i] = max(allData['telePlaceList'][i])
            scoreData['telePlaceAvg'][i] = round(sum(allData['telePlaceList'][i]) / (overview['matchCount'] if overview['matchCount'] else 1), 2)

        
        pickSumList = list(map(sum, allData['pickList']))
        scoreData['telePickAll'] = sum(pickSumList)
        scoreData['telePickMaxItem'] = pickSumList.index(max(pickSumList))
        scoreData['telePickMax'] = max(pickSumList)
        scoreData['telePlaceSuc'] = round(sum(map(sum, allData['telePlaceList'])) / (scoreData['telePickAll'] if scoreData['telePickAll'] else 1), 2)
        scoreData['teleCycle'] = round(sum(allData['cycleList']) / (len(allData['cycleList']) if len(allData['cycleList']) else 1), 2)
        scoreData['teleDockTime'] = round(sum(allData['dockTimerList']) / (overview['matchCount'] if overview['matchCount'] else 1), 2)

        for i in range(overview['matchCount']):
            scoreData['autoDock'][allData['autoDockList'][i]] += 1
            scoreData['teleDock'][allData['teleDockList'][i]] += 1

    return render(request, 'team.html', {
        'teamData': teamData,
        'overview': overview,
        'scoreData': scoreData,
        'scoutData': scoutData,
        'commentData': commentData,
    })

def MatchPage(request, event, level, num):
    matchData = Match.objects.get(id=f'{event}_{level}_{num}')
    scoreList = list(matchData.scores.all())
    sysList = list(matchData.sysScore.all())
    scoutList = list(matchData.scouts.all())

    scoreData = {
        'blue': {
            'grid': [0]*27,
            'gridView': [],
            'start': [],
            'cross': [],
            'mobility': [],
            'autoGridCount': 0,
            'autoGridScore': 0,
            'autoDock': [],
            'autoScore': 0,
            'telePick': [],
            'telePickCount': [],
            'teleGridCount': 0,
            'teleGridScore': 0,
            'endDock': [],
            'endScore': 0,
            'teleScore': 0,
            'link': [False]*27,
            'linkCount': 0,
            'linkScore': 0,
            'coop': False,
            'totalScore': 0
        },
        'red': {
            'grid': [0]*27,
            'gridView': [],
            'start': [],
            'cross': [],
            'mobility': [],
            'autoGridCount': 0,
            'autoGridScore': 0,
            'autoDock': [],
            'autoScore': 0,
            'telePick': [],
            'telePickCount': [],
            'teleGridCount': 0,
            'teleGridScore': 0,
            'endDock': [],
            'endScore': 0,
            'teleScore': 0,
            'link': [False]*27,
            'linkCount': 0,
            'linkScore': 0,
            'coop': False,
            'totalScore': 0
        }
    }

    autoDocked = False
    coopCount = 0
    for score in scoreList:
        side = 'blue' if scoreList.index(score) < 3 else 'red'
        num = scoreList.index(score) if side == 'blue' else scoreList.index(score)-3
        if num == 0:
            autoDocked = False
            coopCount = 0
        grid = score.grid_as_list()
        for i in range(27):
            if grid[i] > 0:
                if scoreData[side]['grid'][i] == 0:
                    scoreData[side]['grid'][i] = grid[i]
                    if grid[i] > 2:
                        scoreData[side]['teleGridCount'] += 1
                        if i > 18:
                            scoreData[side]['teleScore'] += 2
                            scoreData[side]['teleGridScore'] += 2
                        elif i > 9:
                            scoreData[side]['teleScore'] += 3
                            scoreData[side]['teleGridScore'] += 3
                        else:
                            scoreData[side]['teleScore'] += 5
                            scoreData[side]['teleGridScore'] += 5
                    else:
                        scoreData[side]['autoGridCount'] += 1
                        if i > 18:
                            scoreData[side]['autoScore'] += 3
                            scoreData[side]['autoGridScore'] += 3
                        elif i > 9:
                            scoreData[side]['autoScore'] += 4
                            scoreData[side]['autoGridScore'] += 4
                        else:
                            scoreData[side]['autoScore'] += 6
                            scoreData[side]['autoGridScore'] += 6
                    if i%9 > 2 and i%9 < 6:
                        coopCount += 1
                elif grid[i] < 3 and scoreData[side]['grid'][i] > 2:
                    scoreData[side]['grid'][i] = grid[i]
                    scoreData[side]['teleGridCount'] -= 1
                    scoreData[side]['autoGridCount'] += 1
                    if i > 18:
                        scoreData[side]['teleScore'] -= 2
                        scoreData[side]['teleGridScore'] -= 2
                        scoreData[side]['autoScore'] += 3
                        scoreData[side]['autoGridScore'] += 3
                    elif i > 9:
                        scoreData[side]['teleScore'] -= 3
                        scoreData[side]['teleGridScore'] -= 3
                        scoreData[side]['autoScore'] += 4
                        scoreData[side]['autoGridScore'] += 4
                    else:
                        scoreData[side]['teleScore'] -= 5
                        scoreData[side]['teleGridScore'] -= 5
                        scoreData[side]['autoScore'] += 6
                        scoreData[side]['autoGridScore'] += 6

        scoreData[side]['start'].append(score.start)
        scoreData[side]['mobility'].append(score.auto_mobility)
        scoreData[side]['autoScore'] += (3 if score.auto_mobility else 0)
        scoreData[side]['cross'].append([score.cross_cable, score.cross_charge])
        scoreData[side]['telePick'].append(score.pick_as_list())
        scoreData[side]['telePickCount'].append(sum(score.pick_as_list()))
        scoreData[side]['autoDock'].append(score.auto_dock)
        scoreData[side]['autoScore'] += (12 if score.auto_dock == 2 and not autoDocked else (8 if score.auto_dock == 1 and not autoDocked else 0))
        autoDocked = score.auto_dock > 0
        scoreData[side]['endDock'].append(score.end_dock)
        scoreData[side]['endScore'] += (10 if score.end_dock == 3 else (6 if score.end_dock == 2 else (2 if score.end_dock == 1 else 0)))
        scoreData[side]['teleScore'] += (10 if score.end_dock == 3 else (6 if score.end_dock == 2 else (2 if score.end_dock == 1 else 0)))
        scoreData[side]['coop'] = coopCount > 4

    for key, data in scoreData.items():
        for i in range(3):
            for j in range(2, 9):
                if data['grid'][i*9+j] > 0 and data['grid'][i*9+j-1] > 0 and data['grid'][i*9+j-2] and not data['link'][i*9+j-1] and not data['link'][i*9+j-2]:
                    data['link'][i*9+j] = True
                    data['linkScore'] += 5
                    data['totalScore'] += 5
        data['totalScore'] += data['autoScore'] + data['teleScore']
        data['linkCount'] = data['link'].count(True)

    for i in range(9):
        scoreData['blue']['gridView'].append([scoreData['blue']['grid'][j*9+8-i] for j in range(3)])
        scoreData['red']['gridView'].append([scoreData['red']['grid'][(2-j)*9+i] for j in range(3)])

    # print(scoreData['blue']['gridView'])
    return render(request, 'match.html', {
        'matchData': matchData,
        'sysList': sysList,
        'scoreData': scoreData,
        'scoreList': scoreList,
        'scoutList': scoutList
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
            team = Team.objects.filter(id=f'{event}_{request.POST.get("team")}').first()
            if (team != None):
                record.team_data = team

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
                scout.save()

                if teamIdx > 2:
                    sysScore = match.sysScore.last()
                    sysScore.team.add(team)
                    sysScore.save()

        return HttpResponseRedirect(f'/data/{request.POST.get("event_id")}/')