from django.db import models
from django.forms.widgets import MultiWidget, NumberInput, Select
from django import forms
from django.core.validators import ValidationError
from django.contrib.gis.measure import Distance

class DistanceMethods():

    def convert_to_distance_obj(self, string):

        ''' '''

        if string in ['', ' ', None]:
            return None

        s = string.split()
        value = float(s[0])
        unit = s[1]

        if unit == 'km':
            return Distance(km=value)
        elif unit == 'm':
            return Distance(m=value)
        elif unit == 'mi':
            return Distance(mi=value)
        elif unit == 'yd':
            return Distance(yd=value)
        elif unit =='ft':
            return Distance(ft=value)

    def convert_to_string(self, distance_obj):

        ''' '''

        return distance_obj.__str__()

class DistanceSelect(MultiWidget):

    UNIT_CHOICES = [(None, '-------'),
        ('km', 'km'), ('m', 'm'), 
        #('cm', 'cm'),('mm', 'mm'),
        ('mi', 'mi'), ('yd', 'yd'), ('ft', 'ft'),
        #('inch', 'inch'),
        ]

    def __init__(self, *args, **kwargs):

        widgets = (
            NumberInput(),
            Select(choices=self.UNIT_CHOICES)      
            )
        super(DistanceSelect, self).__init__(widgets=widgets, *args, **kwargs)

    def decompress(self, value):

        '''Converts incoming data into formats that the NumberInput and Select widgets can take.'''

        if value == None:
            return [None, None]

        if isinstance(value, Distance):
            value = value.__str__()

        v = value.split()
        return [float(v[0]), v[1]]

class DistanceFormField(forms.Field):

    widget = DistanceSelect

    def clean(self, value):

        print(DistanceMethods().convert_to_distance_obj('%s %s' % (value[0], value[1])))

        if value in [None, '']:
            super(DistanceFormField, self).clean(None)
        else:
            try:
                return DistanceMethods().convert_to_distance_obj('%s %s' % (value[0], value[1]))
            except:
                return ValidationError('Invalid distance')

class DistanceField(models.Field):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(DistanceField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        if isinstance(value, Distance):
            return value
        if not value:
            return None

        return DistanceMethods().convert_to_distance_obj(value)

    def from_db_value(self, value, expression, connection):
       
        return self.to_python(value)

    def get_prep_value(self, value):
        
        return DistanceMethods().convert_to_string(value)

    def db_type(self, connection):

        return 'char(100)'

    def get_internal_type(self):

        return 'CharField'

    def formfield(self, **kwargs):

        defaults = {'form_class':DistanceFormField}
        defaults.update(kwargs)
        return super(DistanceField, self).formfield(**defaults)