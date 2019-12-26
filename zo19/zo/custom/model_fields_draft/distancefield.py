from django.db.models import Field
from django.forms.widgets import MultiWidget, NumberInput, Select
from django import forms
from django.core.validators import ValidationError
from django.contrib.gis.measure import Distance


class DistanceSelect(MultiWidget):

    UNIT_CHOICES = [(None, '-------'),
        ('km', 'km'), ('m', 'm'), ('cm', 'cm'),('mm', 'mm'),
        ('mi', 'mi'), ('yd', 'yd'), ('ft', 'ft'), ('inch', 'inch'),]

    def __init__(self, *args, **kwargs):

        widgets = (
            NumberInput(),
            Select(choices=UNIT_CHOICES)      
            )
        super(DistanceSelect, self).__init__(widgets=widgets, *args, **kwarg)

    def decompress(self, value):

        if value == None:
            return [None, None]
        return [value.value, value.unit]

class DistanceFormField(forms.Field):

    widget = DistanceSelect

    def clean(self, value):

        if None in value or '' in value:
            super(DistanceFormField, self).clean(None)
        else:
            try:
                return Distance('%s%s' % (value.value, value.unit))
            except:
                return ValidationError('Invalid distance')

class DistanceField(Field):

    def to_python(self, value):

        if isinstance(value, Distance):
            return value
        if not value:
            return None
        return Distance(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is not None:
            return 

    def formfield(self, **kwargs):

        defaults = {'form_class':DistanceFormField}
        defaults.update(kwargs)
        return super(DistanceField, self).formfield(**defaults)