from django import forms
from django.utils.translation import ugettext_lazy as _

from zo.models import User

class PasswordResetForm(forms.Form):

    new_password = forms.CharField(label=_("New Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'New Password'}))
    confirm_password = forms.CharField(label=_("Confirm New Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm New Password'}))

