from django.db import models

from zo.models.person.grade import Grade
from zo.models.abstract.place import Address
from zo.models.user import User

class Hub(models.Model):

    ''' '''

    # >>> hub_classification
    name = models.CharField(max_length=100)

    # >>> address
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    main_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='hubs_main_contact')



    def __str__(self):

        return self.name

class HubType(models.Model):

    ''' ??? Bit unsure here... concept thought needed '''

    HUBTYPE_CHOICES = [
        ('School', 'School'),
        ('Club', 'Club'),
        ('Sports Club', 'Sports Club')
        ('Community Organisation', 'Community Organisation'),
        ]

    type = models.CharField(max_length=50, choices=HUBTYPE_CHOICES) # i.e. School, 
    #qualifier = models.CharField(max_length=50, blank=True) # i.e. Sports, Athletics, Secondary, Coeducational, Catholic

    def __str__(self):

        return self.type

class HubClassification(models.Model):

    ''' Each Hub will have it's own HubClassification, even though many of these objects will be
    identical to other Hub.hub_classification's. Classification indicates any appropriate ages, genders and/or 
    ranks that this Hub is for i.e. a NZ Boys Secondary School may have a Grade made up of Male & Trans Male Gender's, 
    and Y9 - Y13 Ranks (inclusive). Each Hub can also declare what name they want to classify their 
    Hub as i.e. Boys Secondary School'''

    name = models.CharField(max_length=50, blank=True)

    hub = models.OneToOneField(Hub, on_delete=models.CASCADE, related_name='hub_classification')
    hub_types = models.ManyToManyField(HubType, related_name='hub_classification')
    grade = models.ForeignKey(Grade, null=True, on_delete=models.SET_NULL, related_name='hub_classifications')

    def __str__(self):

        if self.name != '':
            return self.name
        return self.grade.__str__()


class HubAddress(Address):

    ''' '''

    hub = models.OneToOneField(Hub, on_delete=models.CASCADE, related_name='address')