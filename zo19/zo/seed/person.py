'''  '''

from zo.models.person.gender import Gender
from zo.models.person.grade import AgeGrade, RankGroupType, RankGroup, Rank, Grade
from djangoyearlessdate.models import YearlessDate

from datetime import timedelta, date

class SeedPersonModels():

    def seed_all(self):

        self.seed_genders()
        self.seed_age_grades()
        self.seed_nz_school_ranks()
        self.seed_grades()

    def seed_genders(self):

        ''' '''

        if Gender.objects.all():
            return

        gender_list = ['Female', 'Male', 'Non-Binary']

        for g in gender_list:
            if Gender.objects.filter(gender=g):
                continue
            else:
                Gender(gender=g).save()

    def seed_age_grades(self):

        ''' '''

        if AgeGrade.objects.all():
            return

        # open
        if AgeGrade.objects.filter(open=True):
            pass
        else:
            open = AgeGrade(open=True)
            open.save()

        # create yearless_dates
        yearless_dates = []
        for m in range(1, 13):
            for d in range(1, 32):
                try:
                    YearlessDate(d, m)
                    yearless_dates.append((d,m))
                except:
                    pass

        # dateless age, under and over age with yearless_date
        for a in range(0, 121):

            if len(AgeGrade.objects.filter(age=a).filter(under=None)) == 0:
                AgeGrade(age=a, under=None).save()

            for under in [True, False]:
                for date in yearless_dates:
                    if len(AgeGrade.objects.filter(age=a).filter(under=under).filter(date_day=date[0]).filter(date_month=date[1])) == 0:
                        yless_ag = AgeGrade(age=a, under=under, date_day=date[0], date_month=date[1])
                        yless_ag.save()
                        
    def seed_nz_school_ranks(self):

        '''  '''

        if Rank.objects.all():
            return

        rgt_age = RankGroupType.objects.filter(name='Age')
        if len(rgt_age) == 0:
            rgt_age = RankGroupType(name='Age', description='Rank Groups that have a general "age" aspect to their ranking.')
            rgt_age.save()
        else:
            rgt_age = rgt_age[0]

        rg_nz = RankGroup.objects.filter(name='NZ School Year Levels')
        if len(rg_nz) == 0:
            rg_nz = RankGroup(name='NZ School Year Levels',
                                description='The NZ primary and secondary school year levels, generally for students aged around 5 - 18')
            rg_nz.save()
            rg_nz.types.add(rgt_age)
        else:
            rg_nz = rg_nz[0]

        for i in range(1,14):

            if Rank.objects.filter(name='Year %s' % i).filter(rank_value=i):
                continue

            name = 'Year %s' % i
            Rank(name=name, rank_value=i, rank_group=rg_nz).save()

    def seed_grades(self):

        '''Genders can be multi, ranks can be multi 
        (though as all current ranks are age based, they will not occur with age_grades), 
        age_grades are only 1 '''

        genders = Gender.objects.all()
        age_grades = AgeGrade.objects.all()
        ranks = Rank.objects.all()

