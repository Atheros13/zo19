from django.core.exceptions import ValidationError
from django.forms import CharField, ChoiceField, TextInput
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

class CustomModelChoiceField(ChoiceField):

    def __init__(self, *args, model=None, queryset=None, **kwargs):
        super(CustomModelChoiceField, self).__init__(*args, **kwargs)
        
        ''' A drop down ChoiceField that has the various instances of a set model as options.
        If is_required = False, the 'empty' value is False so that the form itself doesn't auto-demand 
        a value. If the choices should come from a filtered queryset this can be passed and the 
        model choices will be derived from that. '''

        self.model = model
        if queryset == None:
            queryset = self.model.objects.all()

        self.choices = []

        if self.required:
            self.choices.append((None, '---'))
        else:
            self.choices.append((False, '---'))

        if model != None:

            for m in queryset:
                self.choices.append((m.pk, m.__str__()))
      

