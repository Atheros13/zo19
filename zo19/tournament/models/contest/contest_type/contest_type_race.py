from django.db import models
from django.contrib.gis.measure import D, Distance

from zo.custom.model_fields import DistanceUnitField
from tournament.models.contest.contest import ContestType

class ContestTypeRace(ContestType):

    distance_value = models.FloatField()
    distance_unit = DistanceUnitField()
    
    style = models.CharField(max_length=30, blank=True) # Sprint, Walk

    def distance(self):

        unit = self.distance_unit
        value = self.distance_value

        return DistanceUnitField().convert_to_distance(unit, value)