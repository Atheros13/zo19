from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import User, UserSignUp, UserHubSignUp, HubSignUp

''' SignUp Contact Forms have the information required for a request. The process_form() method, 
stored this information in a model i.e. UserHubSignUp and a notice of this requst is sent to info@zo-sports.com. 

ZO-SPORTS can then manually check each request and decide to accept or decline them. If they are accepted, 
the process_signup() method of the model is called, which creates a User and or Hub and associated models, 
and then deletes itself. '''

class UserSignUpContactForm(forms.ModelForm):

    title = 'User Sign Up'
    description = 'Click to sign up as an authenticated user.'
    submit_text = 'Submit Request'

    class Meta:
        model = UserSignUp
        fields = ['firstname', 'surname', 'phone_number', 'email', 'message']

    def process_form(self, request, *args, **kwargs):

        model = self.save(commit=False)

        # Error Check
        if User.objects.filter(email=model.email) or UserSignUp.objects.filter(email=model.email) or UserHubSignUp.objects.filter(email=model.email):
            self.add_error('email', 'The email %s is already used, either for a User or in a sign up request that has not been checked yet.' % model.email)
            return self

        model.save()
        email_message = 'User Only Signup\n\n'
        email_message += 'https://zo-sports.com/confirm_signup/user/%s' % model.id

        send_mail('User Signup', email_message, model.email, ['info@zo-sports.com'])

        return True

class UserHubSignUpContactForm(forms.ModelForm):

    title = 'User & Hub Sign Up'
    description = 'Click to sign up as an authenticated user and to create a new Hub.'
    submit_text = 'Submit Request'

    class Meta():
        model = UserHubSignUp
        fields = ['firstname', 'surname', 'phone_number', 'email',
                  'hub_name', 'hub_type', 'hub_phone_number', 'hub_street', 'hub_towncity',
                  'message']

    def process_form(self, request, *args, **kwargs):

        model = self.save(commit=False)

        # Error Check
        if User.objects.filter(email=model.email) or UserSignUp.objects.filter(email=model.email) or UserHubSignUp.objects.filter(email=model.email):
            self.add_error('email', 'The email %s is already used, either for a User or in a sign up request that has not been checked yet.' % model.email)
            return self

        model.save()
        email_message = 'User & Hub Signup\n\n'
        email_message += 'https://zo-sports.com/confirm_signup/user-hub/%s' % model.id

        return True

class HubSignUpContactForm(forms.ModelForm):

    title = 'Create Hub'
    description = "Click to request to create a new Hub, i.e. a School, Club etc. Please make sure the Hub doesn't already exist."
    submit_text = 'Submit Request'

    class Meta:
        model = HubSignUp
        fields = ['hub_name', 'hub_type', 'hub_phone_number', 'hub_street', 'hub_towncity',
                  'message']

    def process_form(self, request):
        
        ''' '''

        user = request.user
        model = self.save(commit=False)
        model.user = user
        model.save()

        message = 'Hub Signup - Authorised User\n\n'
        message += 'https://zo-sports.com/confirm_signup/hub/%s' % model.id

        send_mail('Hub Signup', message, user.email, ['info@zo-sports.com'])

        return True


