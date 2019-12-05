from django.db.models import CharField

class DistanceUnitField(CharField):

    max_length = 30
    choices = [       
        ('km', 'km'),
        ('m', 'm'),
        ('cm', 'cm'),
        ('mm', 'mm'),
        ('mi', 'mi'),
        ('yd', 'yd'),
        ('ft', 'ft'),
        ('inch', 'inch'),
        ]

