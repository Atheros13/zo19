from django.db.models import Field
from django.forms.widgets import MultiWidget, NumberInput, Select
from django import forms
from django.core.validators import ValidationError
from django.contrib.gis.measure import Distance

class DistanceSelectWidget(MultiWidget):

    UNIT_CHOICES = [(None, '-------'),
        ('km', 'km'), ('m', 'm'), ('cm', 'cm'),('mm', 'mm'),
        ('mi', 'mi'), ('yd', 'yd'), ('ft', 'ft'), ('inch', 'inch'),]

    def __init__(self, *args, **kwargs):

        widgets = (
            NumberInput(),
            Select(choices=UNIT_CHOICES)      
        )
        super(DistanceValueUnitSelect, self).__init__(widgets=widgets, *args, **kwarg)

    def decompress(self, value):

        print(value)

        if value == None:
            return [None, None]
        return [value.value, value.unit]

class DistanceFormField(forms.Field):

    widget = DistanceSelectWidget

    def clean(self, value):

        if None in value or '' in value:
            super(DistanceFormField, self).clean(None)
        else:
            try:
                return Distance('%s%s' % (value.value, value.unit))
            except:
                return ValidationError('Invalid distance')

class DistanceModelField(Field):

    def to_python(self, value):

        if isinstance(value, Distance):
            return value
        if not value:
            return None
        return Distance('%s%s' % (value[0], value[1]))


    def formfield(self, **kwargs):

        defaults = {'form_class':DistanceFormField}
        defaults.update(kwargs)
        return super(DistanceModelField, self).formfield(**defaults)