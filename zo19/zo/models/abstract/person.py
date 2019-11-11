""" 
"""

from django.db import models

class NamePerson(models.Model):

    ''' An abstract class which can be inherited by other models, 
    to be give a person-based "name" to a model i.e. User, HubMember etc. '''

    firstname = models.CharField(verbose_name='First Name', max_length=50)
    middlenames = models.CharField(verbose_name='Middle Name/s', max_length=50, 
                                   blank=True)
    surname = models.CharField(max_length=30)
    
    preferred_name = models.CharField(verbose_name='Preferred Name', max_length=50, 
                                      blank=True, default='')

    class Meta:

        abstract = True

    def __str__(self):
        firstname = self.firstname
        if self.preferred_name:
            firstname = self.preferred_name
        
        return '%s %s' % (firstname, self.surname)

    def name(self):
        if self.preferred_name:
            return self.preferred_name
        return self.firstname

    def fullname(self, preferred=True):

        firstname = self.firstname
        if preferred == True and self.preferred_firstname != '':
            firstname = self.preferred_firstname

        return '%s %s %s' % (firstname, self.middlenames, self.surname)