from django.db import models


class Membership(models.Model):

    ''' '''
    membership_type = None # String() HubRole, HubGroup, Rank
    membership = None # FK() to a specific membership model
    membership_id_number = models.CharField(max_length=50, blank=True)
    # member = model.OneToOneField(???Member, on_delete=models.CASCADE, related_name='???_membership')
    # >>> membership_period

    class Meta:

        abstract = True

    def __str__(self):

        return self.name

class MembershipPeriod(models.Model):

    ''' '''

    # membership = models.OneToOneField(???Membership, on_delete=models.CASCADE, related_name='membership_period')
    start_date = models.DateField()
    end_date = models.DateField(blank=True)

    class Meta:

        abstract = True

    def __str__(self):

        name = '%s: ' % self.membership.__str__()
        if self.start_date:
            name += '%s' % self.start_date
        else:
            return name + 'start and end dates not provided'
        if self.end_date:
            return name + ' - %s' % self.end_date
        return name + ' - currently'