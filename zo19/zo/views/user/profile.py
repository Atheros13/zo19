from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from zo.views.generic.permission import TempPasswordCheck


from datetime import datetime

class UserProfileView(LoginRequiredMixin, TempPasswordCheck, View):

    template_name = 'zo/user/profile.html'

    def get(self, request, *args, **kwargs):

        return render(
            request,
            self.template_name,
            {
                'title':'Profile',
                'year':datetime.now().year,
            }
        )

