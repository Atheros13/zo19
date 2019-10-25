from datetime import datetime
from django.urls import path


from zo import forms, views
from zo.generic.views import PasswordRequestView

urlpatterns = [

    path('password_request/', PasswordRequestView.as_view(), name='password_request'),

]
