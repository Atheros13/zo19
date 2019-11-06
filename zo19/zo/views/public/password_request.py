from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from zo.views.generic import StaffView
from zo.models import User, UserPasswordReset

from datetime import datetime

class PasswordResetView(CreateView):
    
    '''
    '''

    model = UserPasswordReset
    template_name = 'zo/generic/createview.html'
    fields = ['email']

    title = 'Password Reset'
    layout = 'zo/public'
    submit_text = 'Submit Request'
    message = ['If you need to reset your password, please enter your email address and we will email a reset link.']

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.title 
        context['layout'] = '%s/layout.html' % self.layout
        context['year'] = datetime.now().year
        context['submit_text'] = self.submit_text
        context['message'] = self.message

        return context

    def form_valid(self, form):
 
        self.object = form.save(commit=False)
        
        reset_check = UserPasswordReset.objects.filter(email=self.object.email)
        user_check = User.objects.filer(email=self.object.email)
        
        if user_check:
            
            self.object.user = user_check[0]
            self.object.random = None
            
            if reset_check:
                reset_check[0].contact_user()
                return self.post_redirect(title='Password Reset Re-sent', message='Your password reset link has been re-emailed to you')
            else:
                self.object.save()
                return self.post_redirect(title='Password Reset Sent', message='Your password reset link has been emailed to you')

        else:

            return self.post_redirect(title='', message='')

    def post_redirect(self, title='', message=''):

        ''' '''

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':title,
                'message': message,
                'year':datetime.now().year,
            }
        )
