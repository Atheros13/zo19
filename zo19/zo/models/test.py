from django.db import models

from zo.custom.model_fields_draft.distancefield import DistanceField

class Test(models.Model):

    distance = DistanceField()

class Test1(models.Model):

    distance = DistanceField()
    
