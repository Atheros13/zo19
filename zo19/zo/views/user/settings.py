from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from datetime import datetime

from zo.forms.user import UserProfileUpdateForm, UserPasswordChangeForm, UserEmailChangeForm
from zo.views.generic import SelectMultiFormView
from zo.models import UserTemporaryPassword

class UserSettingsView(LoginRequiredMixin, SelectMultiFormView):

    title = 'User Settings'
    forms = [UserProfileUpdateForm, UserPasswordChangeForm, UserEmailChangeForm]
    form_type = 'User Settings'
    layout = 'zo/user'
    message = []
    error_message = []

    def get(self, *args, **kwargs):

        if UserTemporaryPassword.objects.filter(user=self.request.user):
            message.append('You still have a temporary password, you need to change this before continuing')
            form = UserPasswordChangeForm

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