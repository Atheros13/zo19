from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import User

class UserProfileUpdateForm(forms.ModelForm):

    title = 'Update Profile'
    description = 'Click to update profile details'
    submit_text = 'Update Profile'

    class Meta:
        model = User
        fields = []

    def process_form(self, *args, **kwargs):

        model = self.save(commit=False)

        model.save()
        email_message = ''
        email_message += 'https://112.109.84.57:8000/user/confirm_signup'

        send_mail('???', 'no-reply@zo-sports.com', model.email, ['info@zo-sports.com'])

        return True, ['']

class UserPasswordChangeForm(forms.Form):
    
    title = 'Change Password'
    description = 'Click to change your password'
    submit_text = 'Change Password'

    current_password = forms.CharField(label=_("Current Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Current Password'}))
    new_password = forms.CharField(label=_("New Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'New Password'}))
    confirm_password = forms.CharField(label=_("Confirm New Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm New Password'}))

    def process_form(self, *args, **kwargs):

        pass

class UserEmailChangeForm(forms.Form):

    title = 'Change Email'
    description = 'Click to change your email'
    submit_text = 'Change Email'

    current_password = forms.CharField(label=_("Current Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Current Password'}))
    new_email = forms.EmailField(label=_('New Email'),
                                 widget=forms.EmailInput({
                                     'class': 'form-control',
                                     'placeholder':'New Email'}))
    confirm_email = forms.EmailField(label=_('Confirm New Email'),
                                 widget=forms.EmailInput({
                                     'class': 'form-control',
                                     'placeholder':'Confirm New Email'}))

    def process_form(self, *args, **kwargs):

        pass