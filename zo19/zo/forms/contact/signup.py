from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import User, UserSignUp, UserHubSignUp, HubSignUp

class UserSignUpContactForm(forms.ModelForm):

    title = 'User Sign Up'
    description = 'Click to sign up as an authenticated user.'
    submit_text = 'Submit Request'

    class Meta:
        model = UserSignUp
        fields = ['firstname', 'surname', 'phone', 'email', 'message']

    def process_form(self, request, *args, **kwargs):

        model = self.save(commit=False)

        # checks if 
        if User.objects.filter(email=model.email) or UserSignUp.objects.filter(email=model.email) or UserHubSignUp.objects.filter(email=model.email):
            print('here')
            return False, ['The email %s is already used, either for a User or in a sign up request that has not been checked yet.' % model.email]

        model.save()
        email_message = 'User Only Signup\n\n'
        email_message += 'https://zo-sports.com/confirm_signup/user/%s' % model.id

        send_mail('User Signup', email_message, model.email, ['info@zo-sports.com'])

        return True, []

class UserHubSignUpContactForm(forms.ModelForm):

    title = 'User & Hub Sign Up'
    description = 'Click to sign up as an authenticated user and to create a new Hub.'
    submit_text = 'Submit Request'

    class Meta():
        model = UserHubSignUp
        fields = ['firstname', 'surname', 'phone', 'email', #'hub_type', 
                  'hub_name', 'hub_phone', 'hub_street', 'hub_towncity',
                  'message']

    def process_form(self, request, *args, **kwargs):

        model = self.save(commit=False)

        # checks if 
        if User.objects.filter(email=model.email) or UserSignUp.objects.filter(email=model.email) or UserHubSignUp.objects.filter(email=model.email):
            return False, ['The email %s is already used, either for a User or in a sign up request that has not been checked yet.' % model.email]

        model.save()
        email_message = 'User & Hub Signup\n\n'
        email_message += 'https://zo-sports.com/confirm_signup/user-hub/%s' % model.id

        return True, []


class HubSignUpContactForm(forms.ModelForm):

    title = 'Create Hub'
    description = "Click to request to create a new Hub, i.e. a School, Club etc. Please make sure the Hub doesn't already exist."
    submit_text = 'Submit Request'

    class Meta:
        model = HubSignUp
        fields = [#'hub_type',
                    ]

    def process_form(self, user=None):
        
        model = self.save(commit=False)
        model.requester = user
        model.save()

        message = '%s %s %s %s %s' % (model.hub_type, model.name, model.phone, model.email, model.town_city)
        message += '\n%s' % model.id
        message += '\n%s' % user.id
        message += 'https://zo-sports.com/confirm_signup/hub/%s' % model.id

        send_mail('Hub Signup', message, user.email, ['info@zo-sports.com'])

        return True, ['error message']


