from django.shortcuts import render
from django.views import View

from datetime import datetime

class ActionMessageView(View):

    '''  '''

    layout = 'zo'
    title = ''
    message = ''

    def get(self, *args, **kwargs):

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':self.title,
                'message':self.message,
                'year':datetime.now().year,
            }
        )
