from django.db import models
from djangoyearlessdate.models import YearlessDateField

from .gender import Gender


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
    are included in the filter. '''

    open = models.BooleanField(default=False)
    under = models.BooleanField(default=True)
    age = models.PositiveIntegerField(blank=True)
    date = YearlessDateField(blank=True)

    manager = AgeGradeManager()

    def __str__(self):

        pass


class RankGroupType(models.Model):

    ''' Categorises RankGroups i.e. "Age" is used for the NZ School Year Levels, 
    to indicate that these ranks are mostly determined by one's age. '''

    name = models.CharField(max_length=30)

    def __str__(self):

        return self.name

class RankGroup(models.Model):

    ''' The name of a collection of Rank objects. This provides a link 
    between the Ranks and can also assign a type to the Ranks i.e. "Age". '''

    name = models.CharField(max_length=30)
    type = models.ForeignKey(RankGroupType, null=True, on_delete=models.SET_NULL, related_name='rank_groups')

    def __str__(self):

        return self.name

class Rank(models.Model):

    ''' A specific Rank in a RankGroup. Each Rank has to also contain a rank_value, which 
    allows a Rank in a RankGroup to be ordered from lowest to highest. If rank_value is blank, 
    then Ranks should be ordered alphabetically. '''

    name = models.CharField(max_length=30)
    rank_group = models.ForeignKey(RankGroup, on_delete=models.CASCADE, related_name='ranks')
    rank_value = models.PositiveIntegerField(blank=True)

    def __str__(self):

        return '%s %s' % (self.name, self.rank_group.__str__())


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
    genders = models.ManyToManyField(to='zo.Gender', related_name='grades')
    ranks = models.ManyToManyField(Rank, related_name='grades')

    manager = GradeManager()

    def __str__(self):

        pass

