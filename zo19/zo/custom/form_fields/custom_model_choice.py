from django.core.exceptions import ValidationError
from django.forms import ChoiceField
from django.utils.translation import ugettext_lazy as _

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
      

