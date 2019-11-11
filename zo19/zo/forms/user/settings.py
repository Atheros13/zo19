from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from zo.models import Gender, User, UserName
from zo.forms.custom.fields import CustomModelChoiceField, CustomDateField

from datetime import datetime

class UserProfileUpdateForm(forms.Form):

    title = 'Update Profile'
    description = 'Click to update profile details'
    submit_text = 'Update Profile'

    firstname = forms.CharField(label=_('Firstname'), required=True)
    middlenames = forms.CharField(label=_('Middle Names'), required=False)
    surname = forms.CharField(label=_('Surname'), required=True)
    preferred_name = forms.CharField(label=_('Preferred Name'), required=False)

    phone_number = forms.CharField(label=_('Phone Number'), required=False)

    gender = CustomModelChoiceField(label=_('Gender'), model=Gender, required=False)
    dob = CustomDateField(required=False)

    def prepopulate(self, user):

        '''Return a {} of field:values based on the values in the User and UserName models.
        These values are then able to prepopulate the form. '''

        fields = {}

        for field in ['firstname', 'middlenames', 'surname', 'preferred_name']:
            name = UserName.objects.get(user=user)
            if getattr(name, field) not in ['', None]:
                fields[field] = getattr(name, field)

        for field in ['phone_number', 'dob']:
            value = getattr(user, field)
            if value not in ['', None]:
                if field == 'dob':
                    value = value.strftime('%d/%m/%Y')
                fields[field] = value
        
        if user.gender != None:
            fields['gender'] = user.gender.pk

        return fields

    def process_form(self, request, *args, **kwargs):

        user = request.user
        name = UserName.objects.get(user=user)
        for field in ['firstname', 'middlenames', 'surname', 'preferred_name']:
            value = self.cleaned_data[field]
            setattr(name, field, value)
        for field in ['phone_number', 'gender', 'dob']:
            value = self.cleaned_data[field]
            if value not in [None, '']:
                if field == 'gender':
                    value = Gender.objects.get(pk=value)
                setattr(user, field, value)    
        
        user.save()
        name.save()

        return True


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

    def process_form(self, request, *args, **kwargs):

        return True

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

    def process_form(self, request, *args, **kwargs):

        return True
