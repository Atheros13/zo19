from django.db import models

class BaseRankGroupType(models.Model):

    ''' Categorises RankGroups i.e. "Age" is used for the NZ School Year Levels, 
    to indicate that these ranks are mostly determined by one's age. '''

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def __str__(self):

        return self.name

    class Meta:

        abstract = True

class BaseRankGroup(models.Model):

    ''' The name of a collection of Rank objects. This provides a link 
    between the Ranks and can also assign a type to the Ranks i.e. "Age". '''

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    types = models.ManyToManyField(BaseRankGroupType, related_name='rank_groups')

    def __str__(self):

        return self.name

    class Meta:

        abstract = True

class BaseRank(models.Model):

    ''' A specific Rank in a RankGroup. Each Rank has to also contain a rank_value, which 
    allows a Rank in a RankGroup to be ordered from lowest to highest. If rank_value is blank, 
    then Ranks should be ordered alphabetically. '''

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    rank_group = models.ForeignKey(BaseRankGroup, on_delete=models.CASCADE, related_name='ranks')
    rank_value = models.PositiveIntegerField(blank=True)

    def __str__(self):

        return '%s %s' % (self.name, self.rank_group.__str__())

    class Meta:

        abstract = True