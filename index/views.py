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
    return render(request, 'event.html', {
        'selEvent': event,
        'eventData': eventData,
        'matchList': matchList,
    })

def MatchPage(request, event, level, num):
    return render(request, 'match.html', {

    })

def ScoutPage(request, event, level, num, side):
    matchData = Match.objects.get(id=f'{event}_{level}_{num}')
    scoutList = list(SuperScout.objects.filter(target_id=f'{event}_{level}_{num}').all())
    if side == 'blue':
        scoutList = scoutList[0:3]
    elif side == 'red':
        scoutList = scoutList[3:6]

    if request.method == 'POST':
        try:
            for i in range(3):
                scoutList[i].quick = request.POST.getlist('quick')[i]
                scoutList[i].defence = request.POST.getlist('defence')[i]
                scoutList[i].aware = request.POST.getlist('aware')[i]
                scoutList[i].human = request.POST.getlist('human')[i]
                scoutList[i].pick = request.POST.getlist('pick')[i]
                scoutList[i].place = request.POST.getlist('place')[i]
                scoutList[i].foul = request.POST.getlist('foul')[i]
                scoutList[i].other = request.POST.getlist('other')[i]
                scoutList[i].save()
        except:
            return HttpResponseBadRequest()
        return HttpResponseRedirect(f'/data/{event}/')

    return render(request, 'scout.html', {
        'matchData': matchData,
        'scoutList': scoutList,
        'side': side,
    })

def RecordPage(request, event, level, num, robot):
    matchData = Match.objects.get(id=f'{event}_{level}_{num}')
    if robot == 0:
        if request.method == 'POST':
            print({
                'robot': request.POST.get('robot'),
                'team': request.POST.get('team1'),
                'start': request.POST.get('start'),
                'auto_score': request.POST.get('auto_score'),
                'tele_score': request.POST.get('tele_score'),
                'cross_cable': request.POST.get('cross_cable'),
                'cross_charge': request.POST.get('cross_charge'),
                'auto_mobility': request.POST.get('auto_mobility'),
                'auto_docked': request.POST.get('auto_docked'),
                'timer_cycle': request.POST.get('timer_cycle'),
                'tele_trans': request.POST.get('tele_trans'),
            })

            return HttpResponseRedirect(f'/data/{event}/')
        return render(request, 'record.html', {
            'matchData': matchData,
        })
    scoreData = MatchData.objects.get(id=f'{event}_{level}_{num}_{robot}')
    return render(request, 'result.html', {
            'matchData': matchData,
            'scoreData': scoreData,
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
                target_id=matchId,
                id = f'{matchId}_{i}'
            )
            place = (i%3) +1
            SuperScout.objects.create(
                target_id=matchId,
                id = f'{matchId}_{i}',
                quick = place,
                defence = place,
                aware = place,
                human = place,
                pick = place,
                place = place,
            )
        
        return HttpResponseRedirect(f'/data/{request.POST.get("event_id")}/')
    