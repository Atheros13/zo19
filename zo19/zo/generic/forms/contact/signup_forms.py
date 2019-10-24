from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import UserSignUp, UserHubSignUp, HubSignUp

class UserSignUpContactForm(forms.ModelForm):

    title = 'Sign Up'
    description = 'Click to sign up as an authenticated user.'

    class Meta:
        model = UserSignUp
        fields = ['firstname', 'surname', 'phone', 'email', 'message']

    def process_contact(self, *args, **kwargs):

        model = self.save(commit=False)

        # checks if 
        if CustomUser.objects.filter(email=model.email) or UserSignup.objects.filter(email=model.email) or HubUserSignup.objects.filter(email=model.email):
            return False, 'error message'

        model.save()
        email_message = 'User Only Signup\n\n'
        email_message += 'https://112.109.84.57:8000/user/confirm_signup'

        send_mail('User Signup', email_message, model.email, ['info@zo-sports.com'])

        return True, ''

class UserHubSignUpContactForm(forms.ModelForm):

    class Meta():
        model = UserHubSignUp
        fields = ['hub_type', 'hub_name', 'hub_phone', 'hub_address', 'hub_towncity',
                  'firstname', 'surname', 'phone', 'email',
                  'message']

    def process_contact(self, *args, **kwargs):

        model = self.save(commit=False)

        # checks if 
        if CustomUser.objects.filter(email=model.email) or UserSignup.objects.filter(email=model.email) or HubUserSignup.objects.filter(email=model.email):
            return False, 'error message'

        model.save()
        email_message = 'User & Hub Signup\n\n'
        email_message += 'https://112.109.84.57:8000/user/confirm_signup'

        return True, ''

class HubSignUpContactForm(forms.ModelForm):

    title = 'Create Hub'
    description = "Click to request to create a new Hub, i.e. a School, Club etc. Please make sure the Hub doesn't already exist."

    class Meta:
        model = HubSignUp
        fields = ['hub_type', 'name', 'phone', 'email', 'town_city']

    def process_contact(self, user=None):
        
        model = self.save(commit=False)
        model.requester = user
        model.save()

        message = '%s %s %s %s %s' % (model.hub_type, model.name, model.phone, model.email, model.town_city)
        message += '\n%s' % model.id
        message += '\n%s' % user.id

        send_mail('Hub Signup', message, user.email, ['info@zo-sports.com'])

        return True, 'error message'


