"""
Definition of views.
"""

from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View


class ActionMessageView(View):

    def get(self, request, *args, layout='zo', **kwargs):



        return render(
            request,
            'zo/message.html' ,
            {
                'layout':'%s/layout.html' % layout,
                'title':'Success',
                'message':message,
                'year':datetime.now().year,
            }
        )
