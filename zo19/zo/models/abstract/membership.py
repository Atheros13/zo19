from django.db import models


class Membership(models.Model):

    ''' '''
    # <<< type i.e. role, rank, group 
    id_number = models.CharField(max_length=50, blank=True)
    # >>> membership_periods

    class Meta:

        abstract = True

class MembershipPeriod(models.Model):

    ''' '''

    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

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