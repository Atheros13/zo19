from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from datetime import datetime

from zo.forms.user import UserProfileUpdateForm, UserPasswordChangeForm, UserEmailChangeForm
from zo.views.generic import SelectMultiFormView
from zo.models import UserTemporaryPassword

class PasswordResetRedirectButton():

    title = 'Reset Password'
    description = 'Click here to reset your password if you are logged in, but have forgotten your password. (Warning: This will log you out)'

    def process_action(self, request, *args, **kwargs):

        logout(request)

        return redirect('password_request')

class UserSettingsView(LoginRequiredMixin, SelectMultiFormView):

    title = 'User Settings'
    forms = [UserProfileUpdateForm, UserPasswordChangeForm, UserEmailChangeForm]
    extra_actions = [PasswordResetRedirectButton]
    layout = 'zo/user'
    message = []

    def get(self, *args, **kwargs):

        if self.form == UserProfileUpdateForm:
            fields = UserProfileUpdateForm().prepopulate(self.request.user)
            self.form = UserProfileUpdateForm(fields)
        
        # Check Temporary Password
        if UserTemporaryPassword.objects.filter(user=self.request.user):
            message.append('You still have a temporary password, you need to change this before continuing')
            self.form = UserPasswordChangeForm

        return super().get(*args, **kwargs)

    def contact_success(self, form):

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':'Success',
                'message':'Your %s form has been successfully updated' % form.title,
                'year':datetime.now().year,
            }
        )