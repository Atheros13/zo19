from django.db import models

from tournament.models.tournament.tournament import Tournament
from tournament.models.event.event import Event

class TournamentEvent(models.Model):

    ''' '''
    
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tournament_events')




    pass
