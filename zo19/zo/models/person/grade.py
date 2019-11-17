from django.db import models
from djangoyearlessdate.models import YearlessDateField

from .gender import Gender
from zo.models.abstract.base_rank import *


class AgeGradeManager(models.Manager):

    def build_all(self):

        ''' Creates every possible permutation of AgeGrade objects, and 
        fills the database. '''

        # Open Grade
        if not AgeGrade.objects.all().filter(open=True):
            AgeGrade(open=True).save()

        # All dd/mm 
        months = [31,29,31,30,31,30,31,31,30,31,30,31]
        for i in range(len(months)):
            m = i+1
            for d in range(1,i+1):
                
                # get all AgeGrades that have this date
                # check if under=True
                # create under/over versions                
                pass              

class AgeGrade(models.Model):

    ''' An age based filter, if open=True then all ages are included, 
    if under=True, then only ages that are under the date (that year) are included, 
    if under=False, then only ages over (not including) the date (that year) 
    are included in the filter, if under=None then the grade is the age as of datetime.now(). '''

    open = models.NullBooleanField(default=False)
    under = models.NullBooleanField(default=None)
    age = models.PositiveIntegerField(blank=True)
    date = YearlessDateField(blank=True)

    manager = AgeGradeManager()

    def __str__(self):

        if self.open == True:
            return 'Open'
        if self.under == None:
            return '%s Years Old' % self.age
        elif self.under == True:
            return 'Under %s' % self.age
        else:
            return 'Over %s' % self.age



class RankGroupType(BaseRankGroupType):

    ''' Categorises RankGroups i.e. "Age" is used for the NZ School Year Levels, 
    to indicate that these ranks are mostly determined by one's age. '''

    # name
    # description
    pass

class RankGroup(BaseRankGroup):

    ''' The name of a collection of Rank objects. This provides a link 
    between the Ranks and can also assign a type to the Ranks i.e. "Age". '''

    # name
    # description
    types = models.ManyToManyField(RankGroupType, related_name='rank_groups')

class Rank(BaseRank):

    ''' A specific Rank in a RankGroup. Each Rank has to also contain a rank_value, which 
    allows a Rank in a RankGroup to be ordered from lowest to highest. If rank_value is blank, 
    then Ranks should be ordered alphabetically. '''

    # name
    # description
    # rank_value
    rank_group = models.ForeignKey(RankGroup, on_delete=models.CASCADE, related_name='ranks')


class GradeManager(models.Manager):

    def build_all(self):

        ''' Creates every possible permutation of Grade objects, and 
        fills the database. '''
        
        AgeGrade.build_all()

        # recursive functions?

        genders = Gender.objects.all()
        ranks = Rank.objects.all()
        age_grades = AgeGrade.objects.all()
      
class Grade(models.Model):

    ''' A collection of one or more age, gender and/or rank filters. '''

    age = models.ForeignKey(AgeGrade, null=True, on_delete=models.CASCADE, related_name='grades')
    genders = models.ManyToManyField(Gender, related_name='grades')
    ranks = models.ManyToManyField(Rank, related_name='grades')

    manager = GradeManager()

    def __str__(self):

        pass

