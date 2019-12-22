from django.db import models

from tournament.models.contest.contest import Contest
from zo.models.person.grade import Grade

class Event(models.Model):
    
    ''' '''

    contest = modesl.ForeignKey(Contest, on_delete=models.CASCADE, related_name='events')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='events')

    def __str__(self):

        return '%s %s' % (self.grade.__str__(), self.contest.__str__())