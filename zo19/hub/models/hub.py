from django.db import models

from zo.models.person.grade import Grade
from zo.models.abstract.place import Address
from zo.models.user import User

class Hub(models.Model):

    ''' '''

    ## HUB SPECIFICATIONS
    # >>> hub_classification
    name = models.CharField(max_length=100)

    ## HUB CONTACT DETAILS
    # >>> address
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    ## HUB PEOPLE
    # >>> hub_users
    # >>> hub_roles (Main Contact is a Role)
    # >>> hub_rank_groups >>> hub_rank_groups.hub_ranks
    # >>> hub_groups

    def __str__(self):

        return self.name

    def build_hub_type_roles(self, seed=False):

        '''Seed the database with HubRole objects and return the Main Contact HubRole. '''

        from hub.seed.hub import SeedGenericHubRoles

        seed = SeedGenericHubRoles(self, hub_category=self.hub_classification.hub_type.category.__str__())
        return seed.main_contact

class HubTypeCategory(models.Model):

    '''A broad category of Hubs, made up of HubTypes i.e. Education Provider or Club '''

    category = models.CharField(max_length=30, unique=True)

    def __str__(self):

        return self.category

class HubType(models.Model):

    '''The specialised type of Hub, part of HubTypeCategory '''

    category = models.ForeignKey(HubTypeCategory, on_delete=models.CASCADE, related_name='types')
    type = models.CharField(max_length=30)

    def __str__(self):

        return '%s - %s' % (self.category.__str__(), self.type)

class HubClassification(models.Model):

    ''' Each Hub will have it's own HubClassification, even though many of these objects will be
    identical to other Hub.hub_classification's. Classification indicates any appropriate ages, genders and/or 
    ranks that this Hub is for i.e. a NZ Boys Secondary School may have a Grade made up of Male & Trans Male Gender's, 
    and Y9 - Y13 Ranks (inclusive). Each Hub can also declare what name they want to classify their 
    Hub as i.e. Boys Secondary School. '''

    name = models.CharField(max_length=50, blank=True)

    hub = models.OneToOneField(Hub, on_delete=models.CASCADE, related_name='hub_classification')
    hub_type = models.ForeignKey(HubType, null=True, on_delete=models.SET_NULL, related_name='hub_classification')
    grade = models.ForeignKey(Grade, null=True, on_delete=models.SET_NULL, related_name='hub_classifications')

    def __str__(self):

        if self.name != '':
            return self.name
        return self.grade.__str__()


class HubAddress(Address):

    ''' '''

    #line1
    #line2
    #line3 
    #town_city 
    #postcode 
    #country
    hub = models.OneToOneField(Hub, on_delete=models.CASCADE, related_name='address')
