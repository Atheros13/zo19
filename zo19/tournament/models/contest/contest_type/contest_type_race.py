from django.db import models
from django.contrib.gis.measure import D, Distance

from zo.custom.model_fields.custom_distance import CustomDistanceField
from tournament.models.contest.contest import ContestType

class ContestTypeRace(ContestType):

    distance = CustomDistanceField()
    style = models.CharField(max_length=30, blank=True) # Sprint, Walk
