from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import User, UserPasswordRequest

class PasswordRequestForm(forms.ModelForm):

    title = ''
    description = ''
    submit_text = 'Submit Request'

    class Meta:
        model = UserPasswordRequest
        fields = ['email']

    def process_form(self, *args, **kwargs):

        model = self.save(commit=False)

        if False:
            return False, ['error message']

        model.save()
        email_message = ''
        email_message += 'https://112.109.84.57:8000/user/%s/'

        send_mail('???', 'no-reply@zo-sports.com', model.email, ['info@zo-sports.com'])

        return True, ['']

