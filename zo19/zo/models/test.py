from django.db import models

from djangoyearlessdate.models import YearlessDate
from djangoyearlessdate.forms import YearlessDateField

from zo.custom.model_fields.custom_distance import CustomDistanceField

class Test1(models.Model):

    distance = CustomDistanceField()
    yearless = YearlessDateField()

class AnotherTest(models.Model):

    distance = CustomDistanceField()
    yearless = YearlessDateField()

