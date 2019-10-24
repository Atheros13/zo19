"""
Definition of views.
"""

from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View


class PostActionMessage(View):

    def get(self, request, *args, **kwargs):



        return render(
            request,
            'public/message.html',
            {
                'layout':'public/layout.html',
                'title':'Success',
                'message':message,
                'year':datetime.now().year,
            }
        )
