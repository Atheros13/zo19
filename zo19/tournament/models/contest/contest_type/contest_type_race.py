from django.db import models
from django.contrib.gis.measure import D, Distance

from zo.custom.model_fields import DistanceUnitField
from tournament.models.contest.contest import ContestType

class ContestTypeRace(ContestType):

    distance_value = models.FloatField()
    distance_unit = DistanceUnitField()
    style = models.CharField(max_length=30, blank=True)

    def distance(self):
        if self.distance_value != '':
            if self.distance_unit not in ['', None]:
                return Distance('%s%s' % (self.distance_value, self.distance_unit))
        return None