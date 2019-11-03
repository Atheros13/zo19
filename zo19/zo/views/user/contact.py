from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from zo.views.generic.permission import TempPasswordCheck

from zo.forms import BootstrapAuthenticationForm
from zo.forms import GeneralUserContactForm, TechnicalContactForm, HubSignUpContactForm
from zo.views.generic import GenericContactView

from datetime import datetime

class UserContactView(LoginRequiredMixin, TempPasswordCheck, UserPassesTestMixin, GenericContactView):

    template_name = 'zo/generic/contact.html'
    form = None

    title = 'Contact'
    forms = [GeneralUserContactForm, TechnicalContactForm]
    layout = 'zo/user'
    message = []
    error_message = []

    def test_func(self):

        return TempPasswordCheck.test_func(self)

        if self.request.user.is_authorised:
            self.forms.append(HubSignUpContactForm)

        return True
