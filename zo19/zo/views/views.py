"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views import View

class PublicHomeView(View):

    template_name = 'zo/public/index.html'

    def get(request, *args, **kwargs):
        assert isinstance(request, HttpRequest)

        return render(
            request,
            self.template_name,
            {
                'title':'Home Page',
                'year':datetime.now().year,
            }
        )

class PublicAboutView(View):

    template_name = 'zo/public/about.html'

    def get(request, *args, **kwargs):
        """Renders the about page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            self.template_name,
            {
                'title':'About',
                'message':'Your application description page.',
                'year':datetime.now().year,
            }
        )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'zo/generic/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

