from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(MatchData)
admin.site.register(SuperScout)
admin.site.register(SystemScoring)