from django.db import models

from zo.models.person.grade import Grade

class Event(models.Model):
    
    ''' '''

    contest = None
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='events')
