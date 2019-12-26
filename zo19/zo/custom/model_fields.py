from django.db.models import CharField
from django.contrib.gis.measure import D, Distance

class DistanceUnitField(CharField):

    max_length = 5
    choices = [       
        ('km', 'km'),
        ('m', 'm'),
        ('cm', 'cm'),
        #('mm', 'mm'),
        #('mi', 'mi'),
        ('yd', 'yd'),
        ('ft', 'ft'),
        #('inch', 'inch'),
        ]

    def convert_to_distance(self, unit, value):

        if value != '':
            if unit not in ['', None]:
                if unit == 'km':
                    return Distance(km=value)
                elif unit == 'm':
                    return Distance(m=value)
                elif unit == 'yd':
                    return Distance(yd=value)
                elif unit =='ft':
                    return Distance(ft=value)

        return None
