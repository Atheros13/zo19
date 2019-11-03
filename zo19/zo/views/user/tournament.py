from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from zo.views.generic.permission import TempPasswordCheck

from datetime import datetime

class UserTournamentsView(LoginRequiredMixin, TempPasswordCheck, View):

    template_name = 'zo/generic/listview_links.html'

    def get(self, request, *args, **kwargs):

        return render(
            request,
            self.template_name,
            {
                'title':'Tournaments',
                'message': 'Tournament stuff goes here',
                'year':datetime.now().year,
            }
        )