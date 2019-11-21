from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from zo.views.generic import StaffView
from zo.models.signup import UserSignUp, UserHubSignUp, HubSignUp

from datetime import datetime

class ConfirmUserSignUpView(UpdateView, StaffView):
    
    '''
    '''

    model = UserSignUp
    template_name = 'zo/public/confirm_signup.html'
    fields = ['firstname', 'surname', 'phone_number', 'email', 'message', 'is_staff']

    decisions = ['Decline', 'Accept User']
    layout = 'zo/public'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['decisions'] = self.decisions

        context['title'] = '' 
        context['layout'] = '%s/layout.html' % self.layout
        context['year'] = datetime.now().year

        return context

    def form_valid(self, form):
        
        self.object = form.save()

        if self.request.POST.get('Accept User') or self.request.POST.get('Accept Only User'):
            self.object.process_signup(self.request, hub_declined=True)
        elif self.request.POST.get('Accept User & Hub') or self.request.POST.get('Accept Hub'):
            self.object.process_signup(self.request)

        self.object.delete()
        return self.post_redirect()

    def post_redirect(self):

        ''' '''

        for s in [(UserSignUp,'confirm_signup_user'), (UserHubSignUp, 'confirm_signup_user-hub'),
                    (HubSignUp, 'confirm_signup_hub')]:
            queryset = s[0].objects.all()
            if queryset:
                return redirect(s[1], pk=queryset[0].pk)
        
        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':'Done',
                'message':'All SignUp requests have been processed',
                'year':datetime.now().year,
            }
        )

class ConfirmUserHubSignUpView(ConfirmUserSignUpView):

    model = UserHubSignUp
    fields = ['firstname', 'surname', 'phone_number', 'email', 
              'hub_name', 'hub_type', 'hub_phone_number', 'hub_street', 'hub_towncity',
              'message', 'is_staff']
    decisions = ['Decline', 'Decline & Email', 'Accept Only User', 'Accept User & Hub']

class ConfirmHubSignUpView(ConfirmUserHubSignUpView):

    model = HubSignUp
    decisions = ['Decline', 'Decline & Email', 'Accept Hub']
    fields = ['user',
                  'hub_name', 'hub_type', 'hub_phone_number', 'hub_street', 'hub_towncity',
                  'message']