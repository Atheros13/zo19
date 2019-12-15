from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Contest(models.Model):
    
    ''' '''

    CONTENT_TYPE_CHOICES = Q(model__startswith='contest type')

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CONTENT_TYPE_CHOICES)
    object_id = models.PositiveIntegerField()
    contest = GenericForeignKey('content_type', 'object_id') # contest_type ?

    contests = models.ManyToManyField('self')

    def __str__(self):

        pass

class ContestType(models.Model):

    ''' '''

    contest = GenericRelation(Contest)

    class Meta:

        abstract = True

    def __str__(self):
        return self.__class__.__name__