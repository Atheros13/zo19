from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import UserPasswordRequest

class PasswordRequestForm(forms.ModelForm):

    title = ''
    description = ''

    class Meta:
        model = UserPasswordRequest
        fields = ['email']

    def process_form(self, *args, **kwargs):

        model = self.save(commit=False)

        if User.objects.filter(email=model.email) or UserSignup.objects.filter(email=model.email) or HubUserSignup.objects.filter(email=model.email):
            return False, 'error message'

        model.save()
        email_message = ''
        email_message += 'https://112.109.84.57:8000/user/confirm_signup'

        send_mail('???', 'no-reply@zo-sports.com', model.email, ['info@zo-sports.com'])

        return True, ''
