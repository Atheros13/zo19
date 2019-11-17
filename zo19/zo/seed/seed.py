'''  '''

from zo.models.person.gender import Gender
from zo.models.person.grade import AgeGrade, RankGroupType, RankGroup, Rank, Grade

from datetime import timedelta, date

class SeedPersonModels():

    def __init__(self, *args, **kwargs):

        self.genders = []
        self.age_grades = []
        self.ranks = []

        self.seed_genders()
        self.seed_age_grades()
        self.seed_ranks()
        self.seed_grades()

    def seed_genders(self):

        gender_list = ['Female', 'Male', 'Non-Binary', 'Trans-Female', 'Trans-Male']

        for g in gender_list:
            gender_exists = Gender.objects.filter(gender=g)

            if len(gender_exists) > 0:
                self.genders.append(gender_list[0])
            else:
                gender = Gender(gender=g)
                gender.save()
                self.genders.append(gender)

    def seed_age_grades(self):

        ''' '''

        # open
        open = AgeGrade.objects.filter(open=True)
        if open:
            open = open[0]
        else:
            open = AgeGrade(open=True)
            open.save()
        self.age_grades.append(open)

        # create yearless_dates
        yearless_dates = []
        def daterange(start_date, end_date):
            for n in range(int ((end_date - start_date).days)):
                yield start_date + timedelta(n)
        for single_date in daterange(date(2020, 1, 1), date(2021, 1, 1)):
            yearless_dates.append(single_date.strftime("%m/%d"))

        # dateless age, under and over age with yearless_date
        if len(AgeGrade.objects.filter(age=13)) == 0:
            for a in range(0, 121):
                ag = AgeGrade(age=a)
                ag.save()
                self.age_grades.append(ag)

                for under in [True, False]:
                    for date in yearless_dates:
                        yless_ag = AgeGrade(age=a, under=under, date=date)
                        yless_ag.save()
                        self.age_grades.append(yless_ag)              

    def seed_ranks(self):

        '''  '''

        rgt_age = RankGroupType.objects.filter(name='Age')
        if len(rgt_age) == 0:
            rgt_age = RankGroupType(name='Age', description='Rank Groups that have a general "age" aspect to their ranking.')
        else:
            rgt_age = rgt_age[0]

        rg_nz = RankGroup.objects.filter(name='NZ School Year Levels')
        if len(rg_nz) == 0:
            rg_nz = RankGroup(name='NZ School Year Levels',
                                description='The NZ primary and secondary school year levels, generally for students aged around 5 - 18')                
        else:
            rg_nz = rg_nz[0]
            rg_nz.types.add(rgt_age)

        for i in range(1,14):

            if Rank.objects.filter(name='NZ School Year Levels').filter(value=i):
                continue

            name = 'Year %s' % i
            value = i
            Rank(name=name, rank_value=rank, rank_group=rg_nz).save()

    def seed_grades(self):

        pass