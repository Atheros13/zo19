from django.db import models

from zo.models.person.gender import Gender
from zo.models.person.grade import Grade, Rank, RankGroupType
from zo.models.abstract.base_rank import *
from zo.models.abstract.membership import Membership, MembershipPeriod
from zo.models.abstract.person import NamePerson
from zo.models.abstract.role import Role
from zo.models.user import User
from .hub import Hub

from colorful.fields import RGBColorField

from datetime import datetime

### USER

class HubUser(models.Model):

    ''' '''

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_users')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='hubs')

    # >>> name
    gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL, related_name='hub_users')
    dob = models.DateField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    # >>> role_memberships 
    # >>> rank_memberships
    # >>> group_memberships 

    def __str__(self):

        return self.name.__str__()

    def build_from_user_data(self):

        if self.user.gender:
            self.gender = self.user.gender
        if self.user.dob:
            self.dob = self.user.dob
        if self.user.phone_number:
            self.phone_number = self.user.phone_number
        if self.user.email:
            self.email = self.user.email

class HubUserName(NamePerson):

    ''' '''

    hub_member = models.OneToOneField(HubUser, on_delete=models.CASCADE, related_name='name')

    def build_from_user_data(self, user):

        pass

### ROLE

class HubRoleMembership(Membership):

    ''' '''

    hub_user = models.ForeignKey(HubUser, on_delete=models.CASCADE, related_name='role_memberships')
    role = models.ForeignKey('HubRole', on_delete=models.CASCADE, related_name='memberships')
    # id_number (not to be confused with self.id)
    # >>> membership_periods
    requisite_users = models.ManyToManyField(HubUser, related_name='requisite_role_memberships')

    def __init__(self, *args, **kwargs):

        self.hub = self.hub_user.hub

        if self.role.requisite_roll != None:
            self.is_active_membership = self.check_requisite_membership()

    def check_requisite_membership(self):

        ''' Searches all HubUsers in self.requisite_users, searchs all HubRoles, 
        searches all HubRoleMembershipPeriods, and if one of those periods has an end_date 
        attribute which is either None or greater than datetime.now(), returns True. '''

        is_active = False
        while not is_active:
            for user in self.requisite_users:
                for role in user.role_memberships:
                    if role.role == self.role.requisite_role:
                        for period in role.membership_periods:
                            if period.end_date == None or period.end_date > datetime.now():
                                is_active = True

        return is_active

class HubRoleMembershipPeriod(MembershipPeriod):

    ''' A record of a period that a HubUser was in a specific role. There may be multiple periods i.e.
    if a Student was at a school for 1 year, then left and came back 2 years later, the same HubRoleMembership
    would have multiple HubRoleMembershipPeriods. '''

    # start_date
    # end_date
    membership = models.ForeignKey(HubRoleMembership, on_delete=models.CASCADE, related_name='membership_periods')

    def __init__(self, *args, **kwargs):

        pass

class HubRole(Role):

    ''' A position/status/job etc that a HubUser may have in the Hub. 
    This could be Teacher or Student for a school, or Club Member, Treasurer for a Club.
    Part of the Hub creation stage is to automatically create a number of expected HubRoles. 
    
    Some HubRoles require another HubUser to have a current HubRoleMembershipPeriod in a specific HubRole, 
    i.e. a Parent HubRole, requires a linked HubUser that has a current Student HubRole. '''

    # name
    # description
    # >>> memberships
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_roles')
    requisite_role = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='requisite_roles')

    def create_membership(self, hub_user, id_number='', requisite_users=[], start_date=datetime.now(), end_date=''):

        membership = HubRoleMembership(hub_user=hub_user, role=self, id_number=id_number)
        for user in requisite_users:
            membership.requisite_users.add(user)
        membership.save()

        period = HubRoleMembershipPeriod(start_date=start_date, end_date=end_date, membership=self)
        period.save()

### RANK

class HubRankGroup(BaseRankGroup):

    '''  '''
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_rank_groups')
    # >>> hub_ranks
    types = models.ManyToManyField(RankGroupType, related_name='hub_rank_groups')

class HubRank(models.Model):

    ''' A HubRank belongs to a Hub. It can either link to a pre-existing Rank object 
    i.e. Year 9, NZ School System, or each Hub can create their own HubRanks with HubRankGroups 
    i.e. Level 3, Krav Maga Grading. '''

    rank = models.ForeignKey(Rank, null=True, on_delete=models.CASCADE, related_name='hub_ranks')

    hub_rank_name = models.CharField(max_length=30)
    hub_rank_description = models.TextField(blank=True)
    hub_rank_group = models.ForeignKey(HubRankGroup, on_delete=models.CASCADE, related_name='hub_ranks')
    hub_rank_value = models.PositiveIntegerField(blank=True)

    # >>> memberships

    def __init__(self, *args, **kwargs):

        ''' Sets the name, description, rank_group, rank_value attributes based on whether the data is 
        derived from a Rank object or created in the HubRank itself. '''

        if self.rank == None:
            self.name = self.hub_rank_name
            self.description = self.hub_rank_description
            self.rank_group = self.hub_rank_group
            self.rank_value = self.hub_rank_value
        else:
            self.name = self.rank.name
            self.description = self.rank.description
            self.rank_group = self.rank.rank_group
            self.rank_value = self.rank.rank_value

    def __str__(self):

        return '%s %s' % (self.name, self.rank_group.__str__())

class HubRankMembership(Membership):

    ''' '''

    hub_user = models.ForeignKey(HubUser, on_delete=models.CASCADE, related_name='rank_memberships')
    rank = models.ForeignKey(HubRank, on_delete=models.CASCADE, related_name='memberships')

    # id_number (not to be confused with self.id)
    # >>> membership_periods

    def __init__(self, *args, **kwargs):

        self.hub = self.hub_user.hub

class HubRankMembershipPeriod(MembershipPeriod):

    ''' A record of a period that a HubUser had a specific rank. This is usually going to only be one period.
    An example will be a student who is in Year 9 for a year. '''

    # start_date
    # end_date
    membership = models.ForeignKey(HubRankMembership, on_delete=models.CASCADE, related_name='membership_periods')

### GROUP

class HubGroup(models.Model):

    ''' House, Class, School Club, Sports Team'''

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_groups')

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    # >>> ranks
    # >>> roles

    # >>> memberships

    colour = RGBColorField(blank=True)
    text_colour = RGBColorField(colors=['#000000', '#ffffff'], blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


class HubGroupMembership(Membership):

    ''' '''

    # >>> rank_membership_periods
    # >>> role_membership_periods

    # >>> membership_periods 
    # (for HubGroups that either have no role or rank requirements, or this membership doesn't fit any)
    hub_group = models.ForeignKey(HubGroup, on_delete=models.CASCADE, related_name='memberships')

class HubGroupMemberShipPeriods(MembershipPeriod):

    ''' '''

    membership = models.ForeignKey(HubGroupMembership, on_delete=models.CASCADE, related_name='membership_periods')


class HubGroupRank(BaseRank):
    
    ''' '''

    # name
    # description
    # rank_value
    # >>> membership_periods
    rank_group = models.ForeignKey(HubGroup, on_delete=models.CASCADE, related_name='ranks')

    def __init__(self, *args, **kwargs):

        self.hub_group = self.rank_group

class HubGroupRankMembershipPeriod(MembershipPeriod):

    ''' '''

    hub_group_rank = models.ForeignKey(HubGroupRank, on_delete=models.CASCADE, related_name='membership_periods')
    membership = models.ForeignKey(HubGroupMembership, on_delete=models.CASCADE, related_name='rank_membership_periods')


class HubGroupRole(Role):

    ''' '''

    # name
    # description
    # >>> membership_periods
    hub_group = models.ForeignKey(HubGroup, on_delete=models.CASCADE, related_name='roles')

class HubGroupRoleMembershipPeriod(MembershipPeriod):

    ''' '''

    hub_group_role = models.ForeignKey(HubGroupRole, on_delete=models.CASCADE, related_name='membership_periods')
    membership = models.ForeignKey(HubGroupMembership, on_delete=models.CASCADE, related_name='role_membership_periods')
