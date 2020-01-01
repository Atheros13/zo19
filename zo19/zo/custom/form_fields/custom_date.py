from django.core.exceptions import ValidationError
from django.forms import CharField, TextInput
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

class CustomDateField(CharField):

    def __init__(self, *args, **kwargs):
        super(CustomDateField, self).__init__(*args, **kwargs)

        ''' '''

        self.label = _('Date of Birth')
        self.widget = TextInput({'placeholder':'dd/mm/yyyy', })

    def clean(self, value, *args, **kwargs):

        date = super().clean(value)
        if date not in ['', None]:
            try:
                date = datetime.strptime(date, '%d/%m/%Y')
                return date
            except:
                raise ValidationError('Date needs to be in the format dd/mm/yyyy')
        else:
            return date
