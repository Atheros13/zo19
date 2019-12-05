from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

from zo.views.generic.permission import TempPasswordCheck
from django.views import View
from django.views.generic.list import ListView

from hub.models.hub import Hub
from hub.models.hub_user import HubUser

from datetime import datetime

class UserHubsView(LoginRequiredMixin, TempPasswordCheck, View):

    template_name = 'zo/generic/listview_links.html'

    def get(self, request, *args, **kwargs):

        models = Hub.objects.filter(hub_users__user=request.user).order_by('name')

        return render(
            request,
            self.template_name,
            {
                'title':'Hubs',
                'models': models,
                'message': '',
                'year':datetime.now().year,
            }
        )

class REALUserHubView(LoginRequiredMixin, ListView):

    template_name = 'zo/generic/listlinks.html'

    layout = 'zo/user'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Hubs'
        context['year'] = datetime.now().year
        context['layout'] = self.layout

        return context