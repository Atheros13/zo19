''' '''

from zo.models.person.gender import Gender
from zo.models.person.grade import AgeGrade, RankGroupType, RankGroup, Rank, Grade


class SeedPersonModels():

    pass

genders = []
age_grades = []
ranks = []

def seed_genders():

    gender_list = ['Female', 'Male', 'Non-Binary', 'Trans-Female', 'Trans-Male']

    for g in gender_list:
        gender_exists = Gender.objects.filter(gender=g)

        if len(gender_exists) > 0:
            genders.append(gender_list[0])
        else:
            gender = Gender(gender=g)
            gender.save()
            genders.append(gender)

def seed_age_grades():

    # open

    # just age

    # under/over

    pass

def seed_ranks():

    '''NZ School Year ranks. '''

    pass

def seed_grades():

    pass