from django.db import models

# Create your models here.
class Event(models.Model):
    id = models.CharField(max_length=5, primary_key=True, unique=True)
    name = models.CharField(max_length=63, default="")
    week = models.IntegerField(default=1)

    class Meta:
        ordering = ['week', 'id']

class Match(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    level = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    teams = models.TextField(default="")
    score_blue = models.IntegerField(default=0)
    score_red = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def teams_as_list(self):
        return self.teams.split(',')
    
    def level_as_str(self):
        if self.level == 0:
            return 'Pratice'
        elif self.level == 1:
            return 'Quals'
        elif self.level == 2:
            return 'PlayOff'
        else:
            return 'Other'

class MatchData(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    scouter = models.CharField(max_length=30, default="")
    team = models.IntegerField(default=0)
    robot = models.IntegerField(default=0)
    start = models.IntegerField(default=0)
    auto_score = models.TextField(default="")
    tele_score = models.TextField(default="")
    cross_cable = models.BooleanField(default=False)
    cross_charge = models.BooleanField(default=False)
    auto_mobility = models.BooleanField(default=False)
    auto_docked = models.IntegerField(default=0)
    timer_cycle = models.TextField(default="")
    tele_trans = models.IntegerField(default=0)
    tele_fed = models.IntegerField(default=0)
    tele_defended = models.BooleanField(default=False)
    tele_defender = models.CharField(max_length=15, default="")
    tele_pick = models.IntegerField(default=0)
    tele_fail = models.IntegerField(default=0)
    timer_dock = models.TextField(default="")
    end_dock = models.IntegerField(default=0)
    other_link = models.IntegerField(default=0)
    other_immobolity = models.BooleanField(default=False)
    other_comment = models.TextField(default="")
    target = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

class SuperScout(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    quick = models.IntegerField(default=3)
    defence = models.IntegerField(default=3)
    aware = models.IntegerField(default=3)
    human = models.IntegerField(default=3)
    pick = models.IntegerField(default=3)
    place = models.IntegerField(default=3)
    foul = models.CharField(max_length=100, default="")
    other = models.CharField(max_length=100, default="")
    target = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']