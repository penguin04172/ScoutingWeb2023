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
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='matches')

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
        
class SystemScoring(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    red = models.BooleanField(default=False)
    mobility = models.IntegerField(default=0)
    grid = models.IntegerField(default=0)
    charge = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="sysScore")

class Team(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    num = models.IntegerField(default=0)
    name = models.CharField(max_length=60, default="")
    score_max = models.IntegerField(default=0)
    score_avg = models.FloatField(default=0)
    score_rank = models.IntegerField(default=0)
    score_opr = models.IntegerField(default=0)
    auto_start = models.IntegerField(default=0)
    auto_max = models.IntegerField(default=0)
    auto_avg = models.FloatField(default=0)
    auto_top = models.IntegerField(default=0)
    auto_mid = models.IntegerField(default=0)
    auto_bot = models.IntegerField(default=0)
    auto_dock = models.IntegerField(default=0)
    auto_engage = models.IntegerField(default=0)
    tele_max = models.IntegerField(default=0)
    tele_avg = models.FloatField(default=0)
    tele_cycle = models.FloatField(default=0)
    tele_src = models.IntegerField(default=0)
    tele_pick = models.IntegerField(default=0)
    tele_top = models.IntegerField(default=0)
    tele_mid = models.IntegerField(default=0)
    tele_bot = models.IntegerField(default=0)
    tele_success = models.FloatField(default=0)
    end_dock = models.IntegerField(default=0)
    end_engage = models.IntegerField(default=0)
    end_dock_time = models.FloatField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class MatchData(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    team = models.IntegerField(default=0)
    scouter = models.CharField(max_length=30, default="")
    robot = models.IntegerField(default=0)
    start = models.IntegerField(default=0)
    auto_score = models.TextField(default="")
    tele_score = models.TextField(default="")
    cross_cable = models.BooleanField(default=False)
    cross_charge = models.BooleanField(default=False)
    auto_mobility = models.BooleanField(default=False)
    auto_dock = models.IntegerField(default=0)
    timer_cycle = models.TextField(default="")
    tele_trans = models.IntegerField(default=0)
    tele_fed = models.BooleanField(default=False)
    tele_defender = models.CharField(max_length=15, default="")
    tele_pick_fn = models.IntegerField(default=0)
    tele_pick_fb = models.IntegerField(default=0)
    tele_pick_sn = models.IntegerField(default=0)
    tele_pick_sb = models.IntegerField(default=0)
    tele_fail = models.IntegerField(default=0)
    timer_dock = models.TextField(default="")
    end_dock = models.IntegerField(default=0)
    other_link = models.TextField(default="")
    other_immobolity = models.BooleanField(default=False)
    other_tippy = models.BooleanField(default=False)
    other_comment = models.TextField(default="")
    score_auto = models.IntegerField(default=0)
    score_tele = models.IntegerField(default=0)
    score_link = models.IntegerField(default=0)
    score_dock = models.IntegerField(default=0)
    score_grid = models.IntegerField(default=0)
    score_total = models.IntegerField(default=0)
    team_data = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, default=None, related_name='scores')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='scores')

    def robot_as_str(self):
        return f'Red {self.robot-2}' if self.robot>2 else f'Blue {self.robot+1}'
    
    def score_as_list(self):
        score = [0]*27
        ascore = list(map(int, self.auto_score.split(',') if self.auto_score != '' else []))
        tscore = list(map(int, self.tele_score.split(',') if self.tele_score != '' else []))
        for i in tscore:
            if i > 26:
                score[i-9] = 4
            elif i > 18:
                score[i] = 3
            elif i%3 == 1:
                score[i] = 4
            else:
                score[i] = 3
                
        for i in ascore:
            if i > 26:
                score[i-9] = 2
            elif i > 18:
                score[i] = 1
            elif i%3 == 1:
                score[i] = 2
            else:
                score[i] = 1
        return score

    def dock_as_list(self):
        dock = []
        dock.append('None (0)' if self.auto_docked==0 else ('Docked (8)' if self.auto_docked==2 else 'Engaged (12)'))
        dock.append('None (0)' if self.end_dock==0 else ('Parked (2)' if self.end_dock==1 else ('Docked (6)' if self.end_dock==2 else 'Engaged (10)')))
        return dock
        
    def cycle_avg(self):
        cycleList = list(map(float, self.timer_cycle.split(',') if self.timer_cycle != '' else []))
        return round(sum(cycleList)/(len(cycleList) if len(cycleList)>0 else 1), 2)
    
    def defend_as_list(self):
        return list(map(int, self.tele_defender.split(',')))

    class Meta:
        ordering = ['id']

class SuperScout(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    scouter = models.CharField(max_length=30, default="")
    quick = models.IntegerField(default=3)
    defence = models.IntegerField(default=3)
    aware = models.IntegerField(default=3)
    human = models.IntegerField(default=3)
    pick = models.IntegerField(default=3)
    place = models.IntegerField(default=3)
    foul = models.CharField(max_length=100, default="")
    other = models.CharField(max_length=100, default="")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, default=None, related_name='scouts')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='scouts')

    class Meta:
        ordering = ['id']
