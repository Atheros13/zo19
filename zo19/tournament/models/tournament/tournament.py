from django.db import models

from hub.models.hub import Hub
from hub.models.hub_user import HubUser

class Tournament(models.Model):

    ''' '''
    
    # PERMISSIONS
    hubs = models.ManyToManyField(Hub, related_name='tournaments')
    creator = models.ForeignKey(HubUser, null=True, on_delete=models.SET_NULL, related_name='tournaments_create_by')


    

    # >>> competitors
    # >>> tournament_events

    pass
