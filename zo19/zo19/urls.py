"""
Definition of urls for zo19.
"""

from datetime import datetime
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from zo import forms, views


urlpatterns = [

    path('', views.PublicHomeView.as_view(), name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.PublicAboutView.as_view(), name='about'),

    path('login/',
         LoginView.as_view
         (
             template_name='zo/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('admin/', admin.site.urls),

    #path('user/', include('user.urls')),

]
